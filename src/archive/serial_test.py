import threading
import serial
import time

# define the settings for each power supply
PS1_SETTINGS = {'voltage': 10.0, 'current': 0.5}
PS2_SETTINGS = {'voltage': 20.0, 'current': 1.0}
PS3_SETTINGS = {'voltage': 30.0, 'current': 1.5}

# define the COM port for each power supply
PS1_COM_PORT = '/dev/ttyUSB0'
PS2_COM_PORT = '/dev/ttyUSB1'
PS3_COM_PORT = '/dev/ttyUSB2'

# define the baud rate for the power supplies
BAUD_RATE = 9600

# create a serial connection for each power supply
ps1_serial = serial.Serial(PS1_COM_PORT, BAUD_RATE, timeout=1)
ps2_serial = serial.Serial(PS2_COM_PORT, BAUD_RATE, timeout=1)
ps3_serial = serial.Serial(PS3_COM_PORT, BAUD_RATE, timeout=1)

# define a function to set the voltage and current for a power supply
def set_voltage_current(serial_connection, voltage, current):
    serial_connection.write("VSET:{:.1f}\r\n".format(voltage))
    serial_connection.write("ISET:{:.1f}\r\n".format(current))

# define a function to control a power supply in a separate thread
def control_power_supply(serial_connection, settings):
    while True:
        set_voltage_current(serial_connection, settings['voltage'], settings['current'])
        time.sleep(1)

# create a thread for each power supply
ps1_thread = threading.Thread(target=control_power_supply, args=(ps1_serial, PS1_SETTINGS,))
ps2_thread = threading.Thread(target=control_power_supply, args=(ps2_serial, PS2_SETTINGS,))
ps3_thread = threading.Thread(target=control_power_supply, args=(ps3_serial, PS3_SETTINGS,))

# start the threads
ps1_thread.start()
ps2_thread.start()
ps3_thread.start()

# wait for the threads to finish (this won't happen since they run indefinitely)
ps1_thread.join()
ps2_thread.join()
ps3_thread.join()

# close the serial connections
ps1_serial.close()
ps2_serial.close()
ps3_serial.close()
