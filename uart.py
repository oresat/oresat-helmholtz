# ruff: noqa: TRY400

import json

from blink import PICO_LED

REQUEST_DATA_CMD = b'\x33'


def get_mag_field(uart, uart_buf, logger):
    # Initiate handshake
    logger.info("Requesting mag field")
    uart.write(REQUEST_DATA_CMD)

    err = 0
    resp = uart.read(70)

    if resp is not None and len(resp) > 0:
        PICO_LED.value = True
        uart_buf.extend(resp)

        while b'\n' in uart_buf:
            newline_pos = uart_buf.find(b'\n')
            line = uart_buf[:newline_pos]
            uart_buf = uart_buf[newline_pos + 1 :]

            try:
                serialized_data = json.loads(line.decode('ascii'))
                PICO_LED.value = False
                return {
                    "x": serialized_data["x"],
                    "y": serialized_data["y"],
                    "z": serialized_data["z"],
                }

            except UnicodeError as e:
                logger.error("Unicode Error: %s", e)
            except ValueError as e:
                logger.error("Value Error: %s", e)
            except KeyError as e:
                logger.error("Key Error: %s", e)

    PICO_LED.value = False
    return err
