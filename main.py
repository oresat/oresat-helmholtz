from time import sleep

import board
from busio import I2C, UART
from UART import blocking_get_mag_field
from ulab import numpy as np

import adafruit_logging as logging
from ina226 import INA226
from motor import Motor

# Progress spinner
SPINNERS = ["\\", "|", "/", "_"]

# Calibration constants
CAL_DC_STEP = 10  # Decreasing this makes calibration take longer, but increases accuracy

# P-loop tuning constants
PROP_GAIN = 365

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
    LOGGER.info("Running calibration sweep")
    measurements = {
        "x": {"curr": [], "magfield": []},
        "y": {"curr": [], "magfield": []},
        "z": {"curr": [], "magfield": []},
    }

    for plane, assembly in MOTOR_ASSEMBLIES.items():
        LOGGER.info("%s", plane)
        for i in range(1, 100, CAL_DC_STEP):
            print(SPINNERS[i % 4], end="\r\b")  # noqa: T201
            assembly.motor.reverse(i)
            adjusted_field = blocking_get_mag_field(UART)
            curr = assembly.ina226.current
            measurements[plane]["curr"].append(curr)
            measurements[plane]["magfield"].append(adjusted_field[plane])
            assembly.motor.stop()

        for i in range(1, 100, CAL_DC_STEP):
            print(SPINNERS[i % 4], end="\r\b")  # noqa: T201
            assembly.motor.forward(i)
            adjusted_field = blocking_get_mag_field(UART)
            curr = assembly.ina226.current
            measurements[plane]["curr"].append(curr)
            measurements[plane]["magfield"].append(adjusted_field[plane])
            assembly.motor.stop()

    x_currs = np.array(measurements["x"]["curr"])
    y_currs = np.array(measurements["y"]["curr"])
    z_currs = np.array(measurements["z"]["curr"])

    x_fields = np.array(measurements["x"]["magfield"])
    y_fields = np.array(measurements["x"]["magfield"])
    z_fields = np.array(measurements["x"]["magfield"])

    x_line = np.polyfit(x_currs, x_fields, 1)
    y_line = np.polyfit(y_currs, y_fields, 1)
    z_line = np.polyfit(z_currs, z_fields, 1)

    LOGGER.info("x - Slope: %d, Intercept: %d", x_line[0], x_line[1])
    LOGGER.info("y - Slope: %d, Intercept: %d", y_line[0], y_line[1])
    LOGGER.info("z - Slope: %d, Intercept: %d", z_line[0], z_line[1])

    return {
        "x": {"slope": x_line[0], "intercept": x_line[1]},
        "y": {"slope": y_line[0], "intercept": y_line[1]},
        "z": {"slope": z_line[0], "intercept": z_line[1]},
    }


def magfield_p_controller(desired_field):
    """
    Use a p-loop to calculate the current values
    for each plane's motor driver to produce the desired field
    """
    plane_controls = {"x": 1, "y": 1, "z": 1}

    for plane, assembly in MOTOR_ASSEMBLIES.items():
        slope = SLOPES_AND_INTERCEPTS[plane]["slope"]
        intercept = SLOPES_AND_INTERCEPTS[plane]["intercept"]
        # field = slope * amps + intercept -> (field - intercept) / slope = amps
        target_curr = (desired_field[plane] - intercept) / slope
        process_curr = assembly.ina226.current
        err = target_curr - process_curr
        control_output = PROP_GAIN * err
        plane_controls[plane] = control_output

    return plane_controls


SLOPES_AND_INTERCEPTS = run_calibration_sweep()


def print_help():
    LOGGER.info(
        "Available commands:\n\r\
        help: print this message\n\r\
        calibrate: run a calibration sweep\n\r\
        field: create the desired field inside the cage\n\r"
    )


LOGGER.info("Entering main loop")
while True:
    action = input("> ")
    if action == "help":
        print_help()
    elif action == "calibrate":
        SLOPES_AND_INTERCEPTS = run_calibration_sweep()
    elif action == "field":
        LOGGER.info("Enter desired field:")
        # x = input("x (mG): ")
        # y = input("y (mG): ")
        # z = input("z (mG): ")
        x = 250
        y = -250
        z = 100

        try:
            LOGGER.info("Generating field")
            desired_field = {
                "x": float(x),
                "y": float(y),
                "z": float(z),
            }

            prev_duty_cycles = {"x": 1, "y": 1, "z": {}}

            while True:
                try:
                    plane_controls = magfield_p_controller(desired_field)

                    for plane, assembly in MOTOR_ASSEMBLIES.items():
                        plane_ctrl = plane_controls[plane]
                        duty_cycle = prev_duty_cycles[plane]
                        duty_cycle = 1 + abs(int(plane_ctrl))
                        duty_cycle = max(1, min(100, duty_cycle))

                        LOGGER.info("%s: ctrl :%f, dc: %f", plane, plane_ctrl, duty_cycle)

                        if plane_ctrl > 0:
                            assembly.motor.forward(duty_cycle)
                        else:
                            assembly.motor.reverse(duty_cycle)

                        prev_duty_cycles[plane] = duty_cycle

                except KeyboardInterrupt:
                    break

        except TypeError as e:
            LOGGER.error(e)
    else:
        LOGGER.error("Unsupported action. Please try again")
