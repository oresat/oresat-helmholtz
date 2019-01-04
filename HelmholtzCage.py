#!/usr/bin/env python

def magnotometer():
    #import smbus
    #import time
            
    # Get I2C bus
    bus = smbus.SMBus(1)
            
    # MAG3110 address, 0x0E(14)
    # Select Control register, 0x10(16)
    #		0x01(01)	Normal mode operation, Active mode
    bus.write_byte_data(0x0E, 0x10, 0x01)
            
    time.sleep(0.5)
            
    # MAG3110 address, 0x0E(14)
    # Read data back from 0x01(1), 6 bytes
    # X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
    data = bus.read_i2c_block_data(0x0E, 0x01, 6)
            
    # Convert the data
    xMag = data[0] * 256 + data[1]
    if xMag > 32767 :
            xMag -= 65536
            
    yMag = data[2] * 256 + data[3]
    if yMag > 32767 :
            yMag -= 65536

    zMag = data[4] * 256 + data[5]
    if zMag > 32767 :
            zMag -= 65536

    # Output data to screen
    print "Magnetic field in X-Axis : %d" %xMag
    print "Magnetic field in Y-Axis : %d" %yMag
    print "Magnetic field in Z-Axis : %d" %zMag
    
############################################################################

# Sensors located at i2c addresses 0x18 and 0x1c
# Please update if changed
def temperature():

    # Distributed with a free-will license.
    # Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
    # MCP9808
    # This code is designed to work with the MCP9808_I2CS I2C Mini Module available from ControlEverything.com.
    # https://www.controleverything.com/content/Temperature?sku=MCP9808_I2CS#tabs-0-product_tabset-2

    #import smbus
    #import time

    # Get I2C bus
    bus = smbus.SMBus(1)

    # MCP9808 address, 0x18(24)
    # Select configuration register, 0x01(1)
    #		0x0000(00)	Continuous conversion mode, Power-up default
    config = [0x00, 0x00]
    bus.write_i2c_block_data(0x18, 0x01, config)
    # MCP9808 address, 0x18(24)
    # Select resolution rgister, 0x08(8)
    #		0x03(03)	Resolution = +0.0625 / C
    bus.write_byte_data(0x18, 0x08, 0x03)

    time.sleep(0.5)

    # MCP9808 address, 0x18(24)
    # Read data back from 0x05(5), 2 bytes
    # Temp MSB, TEMP LSB
    data = bus.read_i2c_block_data(0x18, 0x05, 2)

    # Convert the data to 13-bits
    ctemp = ((data[0] & 0x1F) * 256) + data[1]
    if ctemp > 4095 :
            ctemp -= 8192
    ctemp = ctemp * 0.0625
    ftemp = ctemp * 1.8 + 32

    # Output data to screen
    print "Sensor 1"
    print "Temperature in Celsius is    : %.2f C" %ctemp
    print "Temperature in Fahrenheit is : %.2f F" %ftemp

    #------------------------------------
    bus.write_i2c_block_data(0x1c, 0x01, config)
    bus.write_byte_data(0x1c, 0x08, 0x03)

    time.sleep(0.5)

    data = bus.read_i2c_block_data(0x1c, 0x05, 2)

    ctemp = ((data[0] & 0x1F) * 256) + data[1]
    if ctemp > 4095 :
            ctemp -= 8192
    ctemp = ctemp * 0.0625
    ftemp = ctemp * 1.8 + 32

    # Output data to screen
    print "Sensor 2"
    print "Temperature in Celsius is    : %.2f C" %ctemp
    print "Temperature in Fahrenheit is : %.2f F" %ftemp

############################################################################

#function to set voltage. 1st parameter is voltage, 2nd is PSU #
def setVolts(voltage, psu):
        
        time.sleep(.1)
        if(psu == 1):
                ser1.write("Asu" + str(voltage * 100) + "\n")
        elif(psu == 2):
                ser2.write("Asu" + str(voltage * 100) + "\n")
        elif(psu == 3): 
                ser3.write("Asu" + str(voltage * 100) + "\n")

#function to set amps. 1st parameter is amps, 2nd is PSU #
def setAmps(amps, psu):
        
        time.sleep(.1)
        if(psu == 1):
                ser1.write("Asi" + str(amps * 1000) + "\n")
        elif(psu == 2):
                ser2.write("Asi" + str(amps * 1000) + "\n")
        elif(psu == 3): 
                ser3.write("Asi" + str(amps * 1000) + "\n")

#function to turn on/off PSU. 1st param: 1 = on, 0 = off, 2nd param: PSU #
def setOutput(onoff, psu):
        
        time.sleep(.1)
        if(psu == 1):
                ser1.write("Aso" + str(onoff) + "\n")
        elif(psu == 2):
                ser2.write("Aso" + str(onoff) + "\n")
        elif(psu == 3): 
                ser3.write("Aso" + str(onoff) + "\n")
        
def turnAllOff():
        
        time.sleep(.1)
        ser1.write("Aso0\n")
        time.sleep(.1)
        ser2.write("Aso0\n")
        time.sleep(.1)
        ser3.write("Aso0\n")
         
                
def turnAllOn():
        
        time.sleep(.1)
        ser1.write("Aso1\n")
        time.sleep(.1)
        ser2.write("Aso1\n")
        time.sleep(.1)
        ser3.write("Aso1\n")

#Power Supply imports
import serial
import time
# Temperature & Magnotometer sensor imports
import smbus

#Initialize serial ports
ser1 = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

print(ser1.name)  

ser2 = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

print(ser2.name)  

ser3 = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

print(ser3.name)  

control = 1

while (control != 0):

        print("\nPlease enter a command.")
        print("0 to Exit program \n1 to set Voltage \n2 to set Amperage")
        print("3 to turn On PSU's \n4 to turn Off PSU's")
        print("5 to check temperature sensors \n6 to check magnetic fields\n")

        try:
                control = int(raw_input('Option selected: '))

                if control == 0:
                        print("\nExiting...")
                      
                elif control == 1:
                        v1 = float(raw_input('Enter desired Voltage: '))
                        p1 = int(raw_input('Select the power supply: '))

                        setVolts(v1, p1)
                        print("\nVoltage set to %s on PSU %d." % (v1, p1))

                elif control == 2:
                        a1 = float(raw_input('Enter desired Amperage: '))
                        p1 = int(raw_input('Select the power supply: '))

                        setAmps(a1, p1)
                        print("\nAmperage set to %s on PSU %d." % (a1, p1))

                elif control == 3:
                        turnAllOn()
                        print("Powering On...")

                elif control == 4:
                        turnAllOff()
                        print("Powering Off...")

                elif control == 5:
                        print("Checking temperatures...")
                        temperature()

                elif control == 6:
                        print("Checking magnotometer")
                        magnotometer()

        except ValueError:
                print("\n***Invalid Entry***")

