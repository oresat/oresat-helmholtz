import serial
import time

# Define the COM port names of the three power supplies
port1 = '/dev/ttyUSB0'
port2 = '/dev/ttyUSB1'
port3 = '/dev/ttyUSB2'

# Open serial connections to the three power supplies
ser1 = serial.Serial(port1, 9600, timeout=1)
ser2 = serial.Serial(port2, 9600, timeout=1)
ser3 = serial.Serial(port3, 9600, timeout=1)

# Set the voltage and current limits for the first power supply
ser1.write(b'VSET1:5.00\n')  # Set voltage to 5V
time.sleep(0.1)
ser1.write(b'ISET1:2.00\n')  # Set current limit to 2A
time.sleep(0.1)

# Set the voltage and current limits for the second power supply
ser2.write(b'VSET1:7.50\n')  # Set voltage to 7.5V
time.sleep(0.1)
ser2.write(b'ISET1:1.50\n')  # Set current limit to 1.5A
time.sleep(0.1)

# Set the voltage and current limits for the third power supply
ser3.write(b'VSET1:3.30\n')  # Set voltage to 3.3V
time.sleep(0.1)
ser3.write(b'ISET1:1.00\n')  # Set current limit to 1A
time.sleep(0.1)

# Close the serial connections
ser1.close()
ser2.close()
ser3.close()
