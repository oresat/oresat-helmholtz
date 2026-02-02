from struct import unpack

from blink import PICO_LED
from cobsr import DecodeError, decode


def get_mag_field(uart):
    resp = uart.read(21)

    if not resp:
        raise ValueError("No response from serial bridge")

    PICO_LED.value = True

    delim_pos = resp.find(b'\x00')

    if delim_pos == -1:
        raise ValueError("Could not parse data from serial bridge")

    packet = resp[:delim_pos]

    try:
        decoded_data = decode(packet)
    except DecodeError as e:
        raise ValueError from e

    try:
        time, x, y, z, mag = unpack('fffff', decoded_data)
    except (RuntimeError, TypeError) as e:
        raise ValueError from e

    PICO_LED.value = False
    return {"time": time, "x": x, "y": y, "z": z, "mag": mag}
