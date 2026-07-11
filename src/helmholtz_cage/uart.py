import sys
from struct import unpack
from time import sleep

from blink import PICO_LED
from cobsr import DecodeError, decode


def get_mag_field(uart):
    resp = uart.read(21)

    if not resp:
        uart.reset_input_buffer()
        raise ValueError("No response from serial bridge")

    PICO_LED.value = True
    delim_pos = resp.find(b'\x00')

    if delim_pos == -1:
        uart.reset_input_buffer()
        raise ValueError(f"Could not parse data from serial bridge: {resp}")

    packet = resp[:delim_pos]

    try:
        decoded_data = decode(packet)
    except DecodeError as e:
        uart.reset_input_buffer()
        raise ValueError from e

    try:
        _time, x, y, z, _mag = unpack('fffff', decoded_data)
    except (RuntimeError, TypeError) as e:
        uart.reset_input_buffer()
        raise ValueError from e

    PICO_LED.value = False
    return (x, y, z)


def blocking_get_mag_field(uart):
    uart.reset_input_buffer()
    while True:
        try:
            return get_mag_field(uart)
        except ValueError:
            continue


def print_bridge_vals(uart):
    try:
        while True:
            try:
                sys.stdout.write(f"\n{blocking_get_mag_field(uart)}")
                sleep(1)
            except KeyboardInterrupt:
                continue
    except KeyboardInterrupt:
        return ""
