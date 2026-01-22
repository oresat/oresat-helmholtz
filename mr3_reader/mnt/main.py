import time
from struct import pack

import constants as const
from serial import Serial, SerialException

from cobsr import encode


def parse_stream(stream):
    """
    Takes in a stream from the mr3 and parses from it the various magnetic field measurement data.
    Uses constants provided from the Alphalabs comms protocol, found in constants.py.
    """
    if len(stream) != 31:
        # Sometimes we get incomplete data that we should ignore
        # This can happen from the serial port timing out, or by requesting a stream too soon/late
        # 5 chunks * 6 bytes each + 1 acknowledge byte = 31 make up a valid stream
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


def wait_for_serial(port, timeout=60):
    time_now = time.time()

    while time.time() - time_now < timeout:
        try:
            ser = Serial(port, 115200, timeout=0.1)
            return ser
        except SerialException:
            print(f"Unable to connect to {port}. Trying again", flush=True)
            time.sleep(1)

    raise SerialException(f"Failed to connect to {port} after {timeout} seconds")


print("Setting up serial ports at /dev/ttyAMA0 and /dev/ttyMR3", flush=True)
mr3_ser = wait_for_serial("/dev/ttyMR3")
rpi_ser = wait_for_serial("/dev/ttyAMA0")

print("Resetting MR3", flush=True)
mr3_ser.write(const.KILL_ALL_PROCESS_CMD)  # Tell the MR3 to stop whatever it's doing
mr3_ser.write(
    const.RESET_TIME_CMD
)  # Start the session by resetting the time per prototocol


print("Sending magnetic field measurements to Pico", flush=True)
try:
    while True:
        stream = mr3_ser.read_until(b"\x08")  # Read data from the MR3

        if stream is not None and len(stream) > 0:
            # Parse, pack, and send to the pico
            data = parse_stream(stream)

            if data is not None:
                packet = pack_data(data)
                if b"\x00" in packet[1:]:
                    print("WARNING: 0 found in packet contents", flush=True)
                else:
                    rpi_ser.write(packet)

        time.sleep(0.5)  # The mr3 sends data at a rate of 2hz

        mr3_ser.write(const.STREAM_DATA_CMD)  # Request the next stream of data
except KeyboardInterrupt:
    pass
finally:
    print("Ending MR3 reader service", flush=True)
