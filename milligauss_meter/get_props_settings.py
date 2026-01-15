# ruff: noqa: T201
import constants as const
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Reset device
ser.write(const.KILL_ALL_PROCESS_CMD)

print("Properties:")
resp = ""
while True:
    # Request Properties
    ser.write(const.ID_METER_PROP_CMD)
    data = ser.read_until(size=21)

    if len(data) > 0:
        if data[-1] != int.from_bytes(const.TERMINATE_BIT):
            resp += data.decode('ascii')
            ser.write(const.ACKNOWLEDGE_CMD)
        else:
            resp += data.decode('ascii')
            break

print(resp.replace(":", "\n").replace("\\x08", ""))

print("Settings:")
resp = ""
while True:
    # Request settings
    ser.write(const.ID_METER_SETT_CMD)
    data = ser.read_until(size=21)

    if len(data) > 0:
        if data[-1] != int.from_bytes(const.TERMINATE_BIT):
            resp += data.decode('ascii')
            ser.write(const.ACKNOWLEDGE_CMD)
        else:
            resp += data.decode('ascii')
            break

print(resp.replace(":", "\n").replace("\\x08", "\n"))
