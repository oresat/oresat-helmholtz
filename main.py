import board
from busio import I2C
from digitalio import DigitalInOut, Direction

import adafruit_logging as logging
from blink import blink_led
from ina226 import INA226
from motor import Motor

logger = logging.getLogger('Helmholtz logger')
logger.setLevel(logging.DEBUG)

logger.info("Oresat Helmholtz Cage Firmware v2")

PICO_LED = DigitalInOut(board.LED)
PICO_LED.direction = Direction.OUTPUT

i2c = I2C(board.GP1, board.GP0)

print(dir(i2c))

# ina226_x = INA226(i2c, 0x40)
# ina226_y = INA226(i2c, 0x41)
# ina226_z = INA226(i2c, 0x42)

motor_x = Motor(in1=board.GP2, in2=board.GP3, led=board.GP13)
motor_y = Motor(in1=board.GP6, in2=board.GP7, led=board.GP14)
motor_z = Motor(in1=board.GP10, in2=board.GP11, led=board.GP15)

while True:
    blink_led(PICO_LED, 1)
