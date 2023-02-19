import serial
import threading
import time

# Define the voltage and current settings for each power supply
settings = {
    "COM1": {"voltage": 5.0, "current": 0.5},
    "COM2": {"voltage": 10.0, "current": 1.0},
    "COM3": {"voltage": 15.0, "current": 1.5},
}

# Define the function to set the voltage and current for a power supply
def set_voltage_current(serial_connection, voltage, current):
    # Send the voltage and current commands to the power supply
    serial_connection.write("VSET:{:.1f}\r\n".format(voltage))
    serial_connection.write("ISET:{:.1f}\r\n".format(current))

    # Read the response from the power supply and print it to the console
    response = serial_connection.readline().strip()
    print response

# Define the function to control the power supplies
def control_power_supply(com_port, voltage, current):
    # Open the serial connection to the power supply
    serial_connection = serial.Serial(com_port, baudrate=9600, timeout=1)

    while True:
        # Set the voltage and current for the power supply
        set_voltage_current(serial_connection, voltage, current)

        # Sleep for 1 second
        time.sleep(1)

# Define the main function
def main():
    # Create a list to hold the threads
    threads = []

    # Create a thread for each power supply and start it
    for com_port, values in settings.items():
        voltage = values["voltage"]
        current = values["current"]
        thread = threading.Thread(target=control_power_supply, args=(com_port, voltage, current))
        thread.start()
        threads.append(thread)

    # Wait for the threads to finish
    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print "Stopping threads..."
        for thread in threads:
            thread.join()
        print "Threads stopped."

if __name__ == '__main__':
    main()
