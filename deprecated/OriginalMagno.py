import smbus
import time

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
print("Magnetic field in X-Axis:", xMag)
print("Magnetic field in Y-Axis:", yMag)
print("Magnetic field in Z-Axis:", zMag)
