import serial
import time

def main():
    ser = serial.Serial('/dev/ttyS0', 9600)
    print("Serial open!")
    try:
        while True: 
            ser.write(b'hi\r\n')
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                print(data.decode())
            time.sleep(0.5)
    finally:
        ser.close()
        print("serial closed -w-")

if __name__ == "__main__":
    main()
