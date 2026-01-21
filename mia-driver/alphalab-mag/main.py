from pprint import pprint

from magnetometer import DebugMagnetometer, Magnetometer

import serial
import time

def main():
    # print("Requesting data stream...")
    # Returns [Time, X, Y, Z, Total]
    # Function actually prints "Time,X,Y,Z,Total" with no spaces
    # Doesn't seem to be a way to get peaks?
    while True:
        prompt = input()
        # prompt = ser.read()
        if prompt == "q":
            break
        elif prompt == "r":
            data = mag.stream_data()
            ser.write(f"{data[0]},{data[1]},{data[2]},{data[3]}\r".encode())
        else:
            print("e")


if __name__ == "__main__":
    global mag
    global props
    global ser
    print("Initializing Serial...")
    ser = serial.Serial('/dev/ttyS0', 9600)
    ser.write(b"Serial Init from RPi Bridge!")
    print("Initializing Magnetometer...")
    try:
        mag = Magnetometer(location="/dev/cu.usbserial-B0011OO5")
    except Exception:
        print(
            "Could not get magnetometer, start in debug mode? This will always return the same data. (y/n): "
        )
        prompt = input()
        if prompt == "y":
            mag = DebugMagnetometer()
        else:
            raise
    print("Reading properties:")
    pprint(mag.meter_properties())
    main()
    ser.close()
