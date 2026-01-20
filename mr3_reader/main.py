# ruff: noqa: T201

import json
import time

import constants as const
import serial


def parse_stream(stream):
    if len(stream) != 31:
        # Sometimes we get incomplete data that we should ignore
        # 5 chunks * 6 bytes each + 1 acknowledge byte = 31 make up a valid stream
        # TODO: Handle incomplete data
        return None

    chunks = [stream[i : i + 6] for i in range(0, len(stream), 6)]

    ret = {
        "time": 0,
        "x": 0,
        "y": 0,
        "z": 0,
        "mag": 0,
    }

    for i, chunk in enumerate(chunks):
        if i == 5:
            # Last byte is the acknowledge byte
            continue

        # First two bytes are config data
        config = chunk[:2]

        # data_null = config[0] & const.NULL_DATA_MSK
        # field_type = (config[0] & const.FIELD_TYPE_MSK) >> 4
        # sett_changed = config[0] & const.SETT_CHANGED_MSK
        sign = config[1] & const.SIGN_MSK
        decimal_place = config[1] & const.DECIMAL_PLACE_MSK

        # Last 3 bytes are the data
        data = int.from_bytes(chunk[2:], byteorder="big") / (10**decimal_place)

        chunk_types = ["time", "x", "y", "z", "mag"]

        ret[chunk_types[i]] = -data if sign else data

    # Convert the data to a json obj that the pico can read, then encode it as utf-8 bytes
    ret = json.dumps(ret)
    ret = ret.encode("ascii")
    ret += b"\n"
    return ret


print("Setting up serial ports...")
mr3_ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)
pico_ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)

print("Resetting MR3")
# Tell the MR3 to stop whatever it's doing
mr3_ser.write(const.KILL_ALL_PROCESS_CMD)
# Start the session by resetting the time per prototocol
mr3_ser.write(const.RESET_TIME_CMD)

print("Entering main loop")
while True:
    # Wait for pico to request mr3 data
    while pico_ser.read_until(b'\x33') is None:
        continue

    # Stream and parse data from the MR3
    stream = mr3_ser.read_until(b"\x08")
    data = parse_stream(stream)

    if data is not None and len(data) > 0:
        # Send to the pico
        bytes_sent = pico_ser.write(data)
        if bytes_sent > 0:
            print(f"Sent {bytes_sent} bytes to Pico: {data}")

    # Request the next stream of data
    mr3_ser.write(const.STREAM_DATA_CMD)
