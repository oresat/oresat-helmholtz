import time

import board
from busio import I2C, UART
from UART import get_mag_field

import adafruit_logging as logging
from ina226 import INA226
from motor import Motor

MAG_FIELD_BUF = bytearray()
MAG_READ_DURATION = 0.5
LAST_MAG_READ_TIME = -1
LAST_MOTOR_DRIVE_TIME = -1
MAG_FIELD = None

LOGGER = logging.getLogger('Helmholtz logger')
LOGGER.setLevel(logging.DEBUG)

LOGGER.info("Oresat Helmholtz Cage Firmware v2")

UART = UART(board.GP16, board.GP17, baudrate=115200, timeout=0.01, receiver_buffer_size=64)
LOGGER.info("Initialized UART")

I2C = I2C(board.GP1, board.GP0)
LOGGER.info("Initialized I2C bus")

INA226_X = INA226(I2C, 0x40)
INA226_Y = INA226(I2C, 0x41)
INA226_Z = INA226(I2C, 0x42)
LOGGER.info("Initialized INA226 drivers")

MOTOR_X = Motor(in1=board.GP2, in2=board.GP3, led=board.GP13)
MOTOR_Y = Motor(in1=board.GP6, in2=board.GP7, led=board.GP14)
MOTOR_Z = Motor(in1=board.GP10, in2=board.GP11, led=board.GP15)
LOGGER.info("Initialized motor drivers")

LOGGER.info("Entering main loop")
while True:
    time_now = time.monotonic()

    if time_now >= 0.25 + LAST_MOTOR_DRIVE_TIME:
        MOTOR_X.reverse(100)
        MOTOR_Y.reverse(100)
        MOTOR_Z.reverse(100)
        LAST_MOTOR_DRIVE_TIME = time_now

    if time_now >= MAG_READ_DURATION + LAST_MAG_READ_TIME:
        try:
            MAG_FIELD_BUF, mag_field = get_mag_field(UART, MAG_FIELD_BUF, LOGGER)
        except ValueError as e:
            LOGGER.error(e)
            continue

        LOGGER.info(["X", "Current:", INA226_X.current, "Bus Voltage:", INA226_X.bus_voltage])
        LOGGER.info(["Y", "Current:", INA226_Y.current, "Bus Voltage:", INA226_Y.bus_voltage])
        LOGGER.info(["Z", "Current:", INA226_Z.current, "Bus Voltage:", INA226_Z.bus_voltage])
        LOGGER.info(mag_field)
        MAG_FIELD = mag_field

        LAST_MAG_READ_TIME = time_now
