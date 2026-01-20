# ruff: noqa: TRY400

import json

from blink import PICO_LED


def get_mag_field(uart, uart_buf, logger):
    PICO_LED.value = True

    mag_field = 0
    bytes_read = uart.read(70)

    if bytes_read is not None and len(bytes_read) > 0:
        uart_buf.extend(bytes_read)

        while b'\n' in uart_buf:
            newline_pos = uart_buf.find(b'\n')
            line = uart_buf[:newline_pos]
            uart_buf = uart_buf[newline_pos + 1 :]

            try:
                serialized_data = json.loads(line.decode('ascii'))
                mag_field = {
                    "x": serialized_data["x"],
                    "y": serialized_data["y"],
                    "z": serialized_data["z"],
                }

            except UnicodeError:
                return mag_field
            except ValueError:
                return mag_field
            except KeyError:
                return mag_field

    # Prevent memory overflows
    if len(uart_buf) > 256:
        uart_buf = bytearray()

    PICO_LED.value = False
    return mag_field
