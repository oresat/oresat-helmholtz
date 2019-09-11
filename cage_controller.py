import serial # Stuff for controlling the power supplies
import time # Stuff for regulated sensor delays
import smbus # Stuff for controlling temperature and magnetic sensors
import utilities as utils # Stuff for debugging and/or general info
from gpiozero import LED

WIRE_WARN_TEMP = 100 # Min cage wire temperatures in F for warning
WIRE_HCF_TEMP = 120 # Max cage wire temperatures in F for forced halting
pin = 'BOARD'

class Coil(): #???
    def __init__(self, psu_index):
        self.in_a = LED(pin + utils.COIL_ADDRS[psu_index][0])
        self.in_b = LED(pin + utils.COIL_ADDRS[psu_index][1])
        self.positive()
    
    def positive(self):
        self.in_b.off()
        self.in_a.on()
    
    def negative(self):
        self.in_a.off()
        self.in_b.on()

class PowerSupply(serial.Serial):
    def __init__(self, port_device, input_delay=utils.INPUT_DELAY, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1):
        serial.Serial.__init__(self, port=str('/dev/' + port_device), baudrate=baudrate, parity=parity, stopbits=stopbits, bytesize=bytesize, timeout=timeout)
        self.port_device = port_device
        self.input_delay = input_delay
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.timeout = timeout
        self.warn_temp = 35 # Min cage wire temperatures in F for warning
        self.halt_temp = 40 # Max cage wire temperatures in F for forced halting
        self.coil = Coil(self.index())

        utils.log(0, 'Initialized Power supply with the following:\n\tPort: ' + str(port_device)
                                                               + '\n\tInput Delay: ' + str(input_delay)
                                                               + '\n\tBaud Rate: ' + str(baudrate)
                                                               + '\n\tParity:' + str(parity)
                                                               + '\n\tStop Bits: ' + str(stopbits)
                                                               + '\n\tByte Size: ' + str(bytesize)
                                                               + '\n\tTimeout: ' + str(timeout))
    def index(self):
        return int(self.port_device[-1]) #???

    def toggle_supply(self, mode):
        utils.log(0, 'Setting ' + self.name + ' to: ' + str(mode))
        self.write(str("Aso" + str(mode) + "\n").encode())

    def set_voltage(self, voltage):
        utils.log(0, 'Setting ' + self.name + ' voltage to: ' + str(voltage) + ' volts.')
        self.write(str("Asu" + str(voltage * 100) + "\n").encode())

    def set_current(self, amperage):
        utils.log(0, 'Setting ' + self.name + ' current to: ' + str(amperage) + ' amps.')
        self.write(str("Asi" + str(abs(amperage) * 1000) + "\n").encode())
        if(amperage < 0): #???
            self.coil.negative()
        else:
            self.coil.positive()

    def check_temperatures():
        utils.log(0, 'Checking ' + self.name + ' temperatures...')

class TemperatureSensor():
    def __init__(self, address, delay=utils.INPUT_DELAY, raw_offset=8192, max_raw=4095,byte_size=2, cont_conv=0x18, power_up=0x01, config=[0x00, 0x00]):
        TemperatureSensor.bus = smbus.SMBus(1)
        TemperatureSensor.is_closed = False
        self.address = address
        self.delay = delay
        self.raw_offset = raw_offset
        self.max_raw = max_raw
        self.byte_size = byte_size
        self.cont_conv = cont_conv
        self.power_up = power_up
        self.config = config

    def __del__(self):
        if(TemperatureSensor.is_closed):
            TemperatureSensor.bus.close()
            TemperatureSensor.is_closed = True


    def read(self):
        time.sleep(self.delay)
        raw_data = TemperatureSensor.bus.read_i2c_block_data(cont_conv, 0x05, self.byte_size)
        temperature = ((raw_data[0] & 0x1F) * 256) + raw_data[1]
        if(temperature > max_raw): temperature -= offset
        return temperature * 0.0625


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
def magnetometer():
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
