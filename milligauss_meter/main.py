# ruff: noqa: T201

import constants as const
import serial


def parse_stream(stream):
    if len(stream) == 31:
        # Sometimes we get incomplete data that we should ignore
        # 5 chunks * 6 bytes each + 1 acknowledge byte = 31 make up a valid stream
        # TODO: Handle incomplete data
        return

    chunks = [stream[i : i + 1] for i in range(0, len(stream), 6)]

    for i, chunk in enumerate(chunks):
        # First two bytes are config data
        config = chunk[:2]
        data_null = config[0] & const.NULL_DATA_MSK
        field_type = config[0] & const.FIELD_TYPE_MSK
        sett_changed = config[0] & const.SETT_CHANGED_MSK
        sign = config[1] & const.SIGN_MSK
        decimal_place = config[1] & const.DECIMAL_PLACE_MSK

        # Last 4 bytes are the data
        data = chunk[2:]

        print(f"Chunk {i}:)")
        print(f"Config: {config}")
        print(f"Data null: {data_null}")
        print(f"Field type: {field_type}")
        print(f"Settings changed: {sett_changed}")
        print(f"Sign: {'+' if sign == 0 else '-'}")
        print(f"Decimal place: {decimal_place}")
        print(f"Data: {data}")


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)

# Tell the MR3 to stop whatever it's doing
ser.write(const.KILL_ALL_PROCESS_CMD)

# Start the session by resetting the time per prototocol
ser.write(const.RESET_TIME_CMD)

while True:
    # Continuously stream and parse valid data from the MR3
    stream = ser.read_until(b'\x08')
    parse_stream(stream)

    # Request the next stream of data
    ser.write(const.STREAM_DATA_CMD)

ser.close()
