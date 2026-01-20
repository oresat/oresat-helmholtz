from struct import unpack

from blink import PICO_LED


def get_mag_field(uart, logger):
    err = 0
    resp = uart.read(20)

    if resp is not None and len(resp) > 0:
        PICO_LED.value = True
        try:
            time, x, y, z, mag = unpack('fffff', resp)
        except RuntimeError as e:
            logger.error(e)
        except TypeError as e:
            logger.error(e)
        else:
            PICO_LED.value = False
            return {"time": time, "x": x, "y": y, "z": z, "mag": mag}

    PICO_LED.value = False
    return err
