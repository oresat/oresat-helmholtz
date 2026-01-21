import time

import board
from busio import I2C, UART

import adafruit_logging as logging
from ina226 import INA226
from motor import Motor
from uart import get_mag_field

logger = logging.getLogger('Helmholtz logger')
logger.setLevel(logging.DEBUG)

logger.info("Oresat Helmholtz Cage Firmware v2")

uart = UART(board.GP16, board.GP17, baudrate=115200, timeout=0.01, receiver_buffer_size=256)
logger.info("Initialized uart: %s", uart)

i2c = I2C(board.GP1, board.GP0)
logger.info("Initialized i2c: %s", i2c)

# ina226_x = INA226(i2c, 0x40)
# ina226_y = INA226(i2c, 0x41)
# ina226_z = INA226(i2c, 0x42)

motor_x = Motor(in1=board.GP2, in2=board.GP3, led=board.GP13)
motor_y = Motor(in1=board.GP6, in2=board.GP7, led=board.GP14)
motor_z = Motor(in1=board.GP10, in2=board.GP11, led=board.GP15)
logger.info("Initialized motor drivers")

mag_field_buf = bytearray()

logger.info("Entering main loop")
while True:
    mag_field_buf, mag_field = get_mag_field(uart, mag_field_buf, logger)

    if mag_field != 0:
        logger.info(mag_field)
