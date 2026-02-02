import time
from struct import pack

import constants as const
import serial

from cobsr import encode


def parse_stream(stream):
    """
    Takes in a stream from the mr3 and parses from it the various magnetic field measurement data.
    Uses constants provided from the Alphalabs comms protocol, found in constants.py.
    """
    if len(stream) != 30:
        # Sometimes we get incomplete data that we should ignore
        # This can happen from the serial port timing out, or by requesting a stream too soon/late
        # 5 chunks * 6 bytes each + 1 acknowledge byte = 31 make up a valid stream
        raise ValueError(f"Invalid stream length received: {len(stream)}")

    chunks = [stream[i : i + 6] for i in range(0, len(stream), 6)]

    data = {
        "time": 0,
        "x": 0,
        "y": 0,
        "z": 0,
        "mag": 0,
    }

    for i, chunk in enumerate(chunks):
        # First two bytes are config data
        config = chunk[:2]

        # Other fields can be parsed, if needed. Eg:
        # data_null = config[0] & const.NULL_DATA_MSK
        # field_type = (config[0] & const.FIELD_TYPE_MSK) >> 4
        # sett_changed = config[0] & const.SETT_CHANGED_MSK
        sign = config[1] & const.SIGN_MSK
        decimal_place = config[1] & const.DECIMAL_PLACE_MSK

        # Last 3 bytes are the data
        sample = int.from_bytes(chunk[2:], byteorder="big") / (10**decimal_place)

        indices = list(data.keys())
        data[indices[i]] = -sample if sign else sample

    return data


def pack_data(data):
    """
    Processes the data from a dict to a COBS-encoded struct
    COBS-encoded data contains no zeros, so we add one as a packet delimiter
    """
    return b"\x00" + encode(
        pack("fffff", data["time"], data["x"], data["y"], data["z"], data["mag"])
    )


print("Setting up serial ports at /dev/ttyAMA0 and /dev/ttyUSB0")
mr3_ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=10)
pico_ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=5)

print("Resetting MR3")
# Tell the MR3 to stop whatever it's doing
mr3_ser.write(const.KILL_ALL_PROCESS_CMD)
# Start the session by resetting the time per prototocol
mr3_ser.write(const.RESET_TIME_CMD)
spare = mr3_ser.read(1)
if spare != const.ACKNOWLEDGE_BIT:
    raise ValueError("Reset didn't acknowledge")

rx_buf = bytearray(64)


print("Sending field measurements to Pico")
try:
    while True:
        stream = mr3_ser.read(30)  # Read data from the MR3

        if not stream:
            raise ValueError("Stream came back empty")

        # Parse, pack, and send to the pico
        data = parse_stream(stream)
        if data is None:
            raise ValueError("Couldn't parse packet")

        print(data)
        packet = pack_data(data)
        if b"\x00" in packet[1:]:
            print("WARNING: 0 found in packet contents")
        else:
            pass
            pico_ser.write(packet)

        framing_byte = mr3_ser.read()
        if framing_byte == const.ACKNOWLEDGE_BIT:
            time.sleep(0.1)
            mr3_ser.write(const.STREAM_DATA_CMD)  # Request the next stream of data
        elif framing_byte == const.TERMINATE_BIT:
            raise ValueError("Received Terminate byte")
        else:
            raise ValueError(f"Unknown byte received: {framing_byte.hex()}")

except KeyboardInterrupt:
    pass
finally:
    print("Ending MR3 reader service")
