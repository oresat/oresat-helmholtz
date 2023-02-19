import serial
import signal
import sys

# Set up the serial connections for each power supply
ser1 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser2 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
ser3 = serial.Serial('/dev/ttyUSB2', 9600, timeout=1)

# Function to handle Ctrl+C
def signal_handler(sig, frame):
    print('\nProgram terminated.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Loop to continuously prompt for voltage and current values and send them to the power supplies
while True:
    try:
        # Prompt for voltage and current values
        voltage = float(raw_input("Enter voltage (V): "))
        current = float(raw_input("Enter current (A): "))

        # Send voltage and current values to each power supply
        ser1.write("VSET:{}\r".format(voltage).encode())
        ser1.write("ISET:{}\r".format(current).encode())
        ser2.write("VSET:{}\r".format(voltage).encode())
        ser2.write("ISET:{}\r".format(current).encode())
        ser3.write("VSET:{}\r".format(voltage).encode())
        ser3.write("ISET:{}\r".format(current).encode())

        # Read voltage and current values from each power supply
        ser1.write("VOUT?\r".encode())
        ser1_voltage = float(ser1.readline().strip())
        ser1.write("IOUT?\r".encode())
        ser1_current = float(ser1.readline().strip())
        ser2.write("VOUT?\r".encode())
        ser2_voltage = float(ser2.readline().strip())
        ser2.write("IOUT?\r".encode())
        ser2_current = float(ser2.readline().strip())
        ser3.write("VOUT?\r".encode())
        ser3_voltage = float(ser3.readline().strip())
        ser3.write("IOUT?\r".encode())
        ser3_current = float(ser3.readline().strip())

        # Display voltage and current values for each power supply
        print("Power Supply 1: Voltage = {:.2f} V, Current = {:.2f} A".format(ser1_voltage, ser1_current))
        print("Power Supply 2: Voltage = {:.2f} V, Current = {:.2f} A".format(ser2_voltage, ser2_current))
        print("Power Supply 3: Voltage = {:.2f} V, Current = {:.2f} A".format(ser3_voltage, ser3_current))
    except KeyboardInterrupt:
        print('\nProgram terminated.')
        sys.exit(0)
    except Exception as e:
        print("Error: {}".format(e))
