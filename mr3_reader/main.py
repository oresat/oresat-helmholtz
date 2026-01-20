# ruff: noqa: T201

from struct import pack
import time

import constants as const
import serial


def parse_stream(stream):
    if len(stream) != 31:
        # Sometimes we get incomplete data that we should ignore
        # 5 chunks * 6 bytes each + 1 acknowledge byte = 31 make up a valid stream
        # TODO: Handle incomplete data
        # print("Data malformed: ", stream.hex(sep=" "))
        return None

    chunks = [stream[i : i + 6] for i in range(0, len(stream), 6)]

    data = {
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
        sample = int.from_bytes(chunk[2:], byteorder="big") / (10**decimal_place)

        chunk_types = ["time", "x", "y", "z", "mag"]

        data[chunk_types[i]] = -sample if sign else sample

    # Convert the data to a json obj that the pico can read, then encode it as ascii bytes
    print(data)
    struct = pack(
        "fffff", data["time"], data["x"], data["y"], data["z"], data["mag"]
    )
    print(len(struct))
    return struct


print("Setting up serial ports...")
mr3_ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.15)
pico_ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=5)

print("Resetting MR3")
# Tell the MR3 to stop whatever it's doing
mr3_ser.write(const.KILL_ALL_PROCESS_CMD)
# Start the session by resetting the time per prototocol
mr3_ser.write(const.RESET_TIME_CMD)

print("Entering main loop")
while True:
    # Read data from the MR3
    stream = mr3_ser.read_until(b"\x08")

    if stream is not None and len(stream) > 0:
        # Parse and send to the pico
        data = parse_stream(stream)
        if data is not None:
            print("Sending data to Pico")
            pico_ser.write(data)

    time.sleep(0.5)
    # Request a stream of data
    mr3_ser.write(const.STREAM_DATA_CMD)
