import serial # Stuff for controlling the power supplies
import time # Stuff for regulated sensor delays
import smbus # Stuff for controlling temperature and magnetic sensors
import magnetic_field_current_relation as mfeq # Stuff for calculating the magnetic field
import utilities as utils # Stuff for debugging and/or general info

WIRE_WARN_TEMP = 100 # Min cage wire temperatures in F for warning
WIRE_HCF_TEMP = 120 # Max cage wire temperatures in F for forced halting

class PowerSupply(serial.Serial):
    def __init__(self, i_port_device, i_input_delay=utils.INPUT_DELAY, i_baudrate=9600, i_parity=serial.PARITY_NONE, i_stopbits=serial.STOPBITS_ONE, i_bytesize=serial.EIGHTBITS, i_timeout=1):
        serial.Serial.__init__(self, port=str('/dev/' + i_port_device), baudrate=i_baudrate, parity=i_parity, stopbits=i_stopbits, bytesize=i_bytesize, timeout=i_timeout)
        self.warn_temp = 35 # Min cage wire temperatures in F for warning
        self.halt_temp = 40 # Max cage wire temperatures in F for forced halting

        port_device = i_port_device
        input_delay = i_input_delay
        baudrate = i_baudrate
        parity = i_parity
        stopbits = i_stopbits
        bytesize = i_bytesize
        timeout = i_timeout
        warn_temp = self.warn_temp
        halt_temp = self.halt_temp

        utils.log(0, 'Initialized Power supply with the following:\n\tPort: ' + str(port_device)
                                                               + '\n\tInput Delay: ' + str(input_delay)
                                                               + '\n\tBaud Rate: ' + str(baudrate)
                                                               + '\n\tParity:' + str(parity)
                                                               + '\n\tStop Bits: ' + str(stopbits)
                                                               + '\n\tByte Size: ' + str(bytesize)
                                                               + '\n\tTimeout: ' + str(timeout))

    def toggle_supply(mode):
        utils.log(0, 'Setting ' + port_device + ' active to: ' + str(mode))
        self.write("Aso" + str(mode) + "\n")

    def set_voltage(voltage):
        utils.log(0, 'Setting ' + port_device + ' voltage to: ' + str(voltage) + ' volts.')
        self.write("Asu" + str(voltage * 100) + "\n")

    def set_current(amperage):
        utils.log(0, 'Setting ' + port_device + ' current to: ' + str(amperage) + ' amps.')
        self.write("Asi" + str(amps * 1000) + "\n")

    def check_temperatures():
        utils.log(0, 'Checking ' + port_device + ' temperatures...')

# data conversion processes for magnetometer and temperature
def checksize(measurement, maxval, offset):
    if measurement > maxval :
        return measurement - offset
    else:
        return measurement

# function to safety check temperatures
def temperature_check_bounds(temp, warning, shutoff):
    if temp > warning:
        utils.log(1, "Reached minimum warning temperature! Try turning off the cage to let it cool off?")
        if temp > shutoff:
            utils.log(1, "Reached maximum warning temperature! Auto-powering down the cage!")
            toggle_all_power_supply(0)

# function to get magnetic field components from sensors
def magnotometer():
    # Get I2C bus
    bus = smbus.SMBus(1)
    time.sleep(utils.INPUT_DELAY)

    # MAG3110 address, 0x0E(14)
    # Select Control register, 0x10(16)
    #        0x01(01)    Normal mode operation, Active mode
    bus.write_byte_data(0x0E, 0x10, 0x01)
    time.sleep(utils.INPUT_DELAY)
    # MAG3110 address, 0x0E(14)
    # Read data back from 0x01(1), 6 bytes
    # X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
    data = bus.read_i2c_block_data(0x0E, 0x01, 6)

    # Convert the data
    xMag = data[0] * 256 + data[1]
    xMag = checksize(xMag, 32767, 65536)

    yMag = data[2] * 256 + data[3]
    yMag = checksize(yMag, 32767, 65536)

    zMag = data[4] * 256 + data[5]
    zMag = checksize(zMag, 32767, 65536)

    # divide by 10 to convert bit counts to microteslas
    return xMag/10, yMag/10, zMag/10

# function to get (and check) temperatures from sensors
# Sensors located at i2c addresses 0x18 and 0x1c
# Please update if changed
def temperature():
    # 1st sensor for wire temp
    # Distributed with a free-will license.
    # Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
    # MCP9808
    # This code is designed to work with the MCP9808_I2CS I2C Mini Module available from ControlEverything.com.
    # https://www.controleverything.com/content/Temperature?sku=MCP9808_I2CS#tabs-0-product_tabset-2

    # Get I2C bus
    bus = smbus.SMBus(1)

    # MCP9808 address, 0x18(24)
    # Select configuration register, 0x01(1)
    #        0x0000(00)    Continuous conversion mode, Power-up default
    config = [0x00, 0x00]
    bus.write_i2c_block_data(0x18, 0x01, config)
    # MCP9808 address, 0x18(24)
    # Select resolution rgister, 0x08(8)
    #        0x03(03)    Resolution = +0.0625 / C
    bus.write_byte_data(0x18, 0x08, 0x03)

    time.sleep(0.2)

    # MCP9808 address, 0x18(24)
    # Read data back from 0x05(5), 2 bytes
    # Temp MSB, TEMP LSB
    data = bus.read_i2c_block_data(0x18, 0x05, 2)

    # Convert the data to 13-bits
    ctemp1 = ((data[0] & 0x1F) * 256) + data[1]
    ctemp1 = checksize(ctemp1, 4095, 8192)
    ctemp1 = ctemp1 * 0.0625

    # 2nd sensor for PSU temp
    #------------------------------------
    bus.write_i2c_block_data(0x1c, 0x01, config)
    bus.write_byte_data(0x1c, 0x08, 0x03)

    time.sleep(0.2)

    data = bus.read_i2c_block_data(0x1c, 0x05, 2)

    ctemp2 = ((data[0] & 0x1F) * 256) + data[1]
    ctemp2 = checksize(ctemp2, 4095, 8192)
    ctemp2 = ctemp2 * 0.0625

    # wire: 100 warn-120 danger, psu: 35 warn-40 danger
    temperature_check_bounds(ctemp1, WIRE_WARN_TEMP, WIRE_HCF_TEMP)
    temperature_check_bounds(ctemp2, PSU_WARN_TEMP, PSU_HCF_TEMP)
    return ctemp1, ctemp2

def poll_data(duration = 10.0, dt = 1.0):
    time_step = [0.0]
    # temp_array = [temperature()]
    mag_array = [magnotometer()]
    while time_step[-1] < duration:
        time.sleep(dt)
        time_step.append(time_step[-1] + dt)
        # temp_array.append(temperature())
        mag_array.append(magnotometer())
    return time_step, mag_array #temp_array, mag_array

def print_data():
    time, mag = poll_data(20, 1)
    i = 0
    for t in time:
        print(time[i], mag[i])
        i += 1

#
# Legacy cage controller interface
#   (Can be used by specifying `cli` in the driver)
#
def cli_menu(control):
    if control == 0:
        print("\nExiting...")
    elif control == 1:
        v1 = float(input('Enter desired Voltage: '))
        p1 = int(input('Select the power supply: '))
        set_volts(v1, p1)
        log(0, "\nVoltage set to %s on PSU %d." % (v1, p1))
    elif control == 2:
        a1 = float(input('Enter desired Amperage: '))
        p1 = int(input('Select the power supply: '))
        set_amps(a1, p1)
        log(0, "\nAmperage set to %s on PSU %d." % (a1, p1))
    elif control == 3:
        toggle_all_power_supply(1)
        log(0, "Powering On...")
    elif control == 4:
        toggle_all_power_supply(0)
        log(0, "Powering Off...")
    elif control == 5:
        log(0, "Checking temperatures...")
        ctemp1, ctemp2 = temperature()
        # Output data to screen
        print("Sensor 1")
        print("Temperature in Celsius is    : %.2f C") % ctemp1
        print("Temperature in Fahrenheit is : %.2f F") % utils.c_to_f(ctemp1)
        print("Sensor 2")
        print("Temperature in Celsius is    : %.2f C") % ctemp2
        print("Temperature in Fahrenheit is : %.2f F") % utils.c_to_f(ctemp2)
    elif control == 6:
        print("Checking magnotometer, units in microTeslas")
        xMag, yMag, zMag = magnotometer()
        # Output data to screen
        print("Magnetic field in X-Axis : %d") % xMag
        print("Magnetic field in Y-Axis : %d") % yMag
        print("Magnetic field in Z-Axis : %d") % zMag
    elif control == 7:
        #ps3=x, ps2=y, ps1=z
        ps2, ps1, ps3 = mfeq.fieldToCurrent(x0, y0, z0)
        set_amps(ps1, 1)
        set_amps(ps2, 2)
        set_amps(ps3, 3)
        print("\nAmperage set to %s on PSU %d." % (ps1, 1))
        print("\nAmperage set to %s on PSU %d." % (ps2, 2))
        print("\nAmperage set to %s on PSU %d." % (ps3, 3))
    elif control == 8:
        print_data()
    elif control == 9:
        plot_graph()

# function for interacting with the user
def interface():
    control = 1
    while (control != 0):
        print("\nPlease enter a command.")
        print("0 to Exit program \n1 to set Voltage \n2 to set Amperage")
        print("3 to turn On PSU's \n4 to turn Off PSU's")
        print("5 to check temperature sensors \n6 to check magnetic fields")
        print("7 to set a uniform magnetic field\n8 to print some data")
        print("9 to plot a graph\n")

        try:
            control = int(input('Option selected: '))
            cli_menu(control)
        except ValueError:
            print("\n***Invalid Entry***")
