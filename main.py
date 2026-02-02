import time

import board
from busio import I2C, UART
from UART import get_mag_field
from ulab import numpy as np

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

UART = UART(board.GP16, board.GP17, baudrate=115200, timeout=10, receiver_buffer_size=128)
LOGGER.info("Initialized UART")

I2C = I2C(board.GP1, board.GP0)
LOGGER.info("Initialized I2C bus")

INA226_X = INA226(I2C, 0x40)
INA226_Y = INA226(I2C, 0x41)
INA226_Z = INA226(I2C, 0x42)

MOTOR_X = Motor(in1=board.GP2, in2=board.GP3, led=board.GP13)
MOTOR_Y = Motor(in1=board.GP6, in2=board.GP7, led=board.GP14)
MOTOR_Z = Motor(in1=board.GP10, in2=board.GP11, led=board.GP15)


class MotorDriverAssembly:
    def __init__(self, motor, ina226):
        self.motor = motor
        self.ina226 = ina226


MOTOR_ASSEMBLIES = {
    "x": MotorDriverAssembly(MOTOR_X, INA226_X),
    "y": MotorDriverAssembly(MOTOR_Y, INA226_Y),
    "z": MotorDriverAssembly(MOTOR_Z, INA226_Z),
}
LOGGER.info("Initialized motor driver assemblies")


def run_calibration_sweep():
    measurements = {
        "x": {"curr": [], "magfield": []},
        "y": {"curr": [], "magfield": []},
        "z": {"curr": [], "magfield": []},
    }

    for plane, asmbly in MOTOR_ASSEMBLIES.items():
        LOGGER.info(plane)
        for i in range(1, 100, 5):
            asmbly.motor.reverse(i)
            while True:
                try:
                    adjusted_field = get_mag_field(UART)
                    break
                except ValueError:
                    continue
            curr = asmbly.ina226.current
            LOGGER.info(curr)
            measurements[plane]["curr"].append(curr)
            measurements[plane]["magfield"].append(adjusted_field[plane])
            asmbly.motor.stop()

        for i in range(1, 100, 5):
            asmbly.motor.forward(i)
            while True:
                try:
                    adjusted_field = get_mag_field(UART)
                    break
                except ValueError:
                    continue
            curr = asmbly.ina226.current
            LOGGER.info(curr)
            measurements[plane]["curr"].append(curr)
            measurements[plane]["magfield"].append(adjusted_field[plane])
            asmbly.motor.stop()

    x_currs = np.array(measurements["x"]["curr"])
    y_currs = np.array(measurements["y"]["curr"])
    z_currs = np.array(measurements["z"]["curr"])
    x_fields = np.array(measurements["x"]["magfield"])
    y_fields = np.array(measurements["x"]["magfield"])
    z_fields = np.array(measurements["x"]["magfield"])

    x_line = np.polyfit(x_currs, x_fields, 1)
    y_line = np.polyfit(y_currs, y_fields, 1)
    z_line = np.polyfit(z_currs, z_fields, 1)

    LOGGER.info("X - Slope: %d, Intercept: %d", x_line[0], x_line[1])
    LOGGER.info("Y - Slope: %d, Intercept: %d", y_line[0], y_line[1])
    LOGGER.info("Z - Slope: %d, Intercept: %d", z_line[0], z_line[1])


LOGGER.info("Running calibration sweep")
run_calibration_sweep()

# LOGGER.info("Entering main loop")
