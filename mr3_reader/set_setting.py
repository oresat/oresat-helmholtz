# ruff: noqa: T201
# AVBL_FREQS=0,,2,5,10,20,30,40,60120
import constants as const
import numpy as np
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=3)

freq = np.uint16(1)

# Reset device
ser.write(const.KILL_ALL_PROCESS_CMD)

ser.write(const.ALTER_METER_SETT_BIT + const.ALTER_STREAM_PERIOD_BIT + 2*b'\x00' + freq)

res = ser.read(1)

print(res)
