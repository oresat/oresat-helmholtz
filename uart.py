from struct import unpack

from blink import PICO_LED
from cobsr import DecodeError, decode


def get_mag_field(uart, buf, logger):
    err = 0
    resp = uart.read(64)

    if resp is not None and len(resp) > 0:
        PICO_LED.value = True

        buf.extend(resp)
        delim_pos = buf.find(b'\x00')

        if delim_pos != -1 and len(buf) >= delim_pos + 21:
            packet = buf[delim_pos + 1 : delim_pos + 21]

            new_buf = buf[delim_pos + 21 :]

            try:
                decoded_data = decode(packet)
            except DecodeError as e:
                # logger.error(e)
                return new_buf, err
            else:
                try:
                    time, x, y, z, mag = unpack('fffff', decoded_data)
                except (RuntimeError, TypeError) as e:
                    logger.error("Unpack error: %s", e)
                    return new_buf, err
                else:
                    PICO_LED.value = False
                    return new_buf, {"time": time, "x": x, "y": y, "z": z, "mag": mag}

    PICO_LED.value = False
    return buf, err
