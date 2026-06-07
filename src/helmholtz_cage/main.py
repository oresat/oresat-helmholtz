import sys
from time import sleep

import board
import usb_cdc
from busio import I2C, UART
from data import print_curr_mag_csv, print_dci_csv, print_fields_csv
from ina226 import INA226
from motor import Motor
from UART import blocking_get_mag_field
from ulab import numpy as np

import adafruit_logging as logging

# Calibration constants
CAL_DC_STEP = 10

# P-loop tuning constants
PROP_GAIN = 25

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
        self.ina226.calibrate(r_shunt_ohms=0.03, max_expected_amps=2.0)


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
        for i in range(0, 101, CAL_DC_STEP):
            print(f"\rCalibrating {plane} plane {int((i / 200) * 100)}%", end=" " * 20)
            assembly.motor.reverse(i)
            curr = assembly.ina226.current
            sleep(0.5)
            adjusted_field = blocking_get_mag_field(UART)
            measurements[plane]["curr"].append(curr)
            measurements[plane]["magfield"].append(adjusted_field[plane])

        assembly.motor.stop()

        for i in range(0, 101, CAL_DC_STEP):
            print(f"\rCalibrating {plane} plane {int(((100 + i) / 200) * 100)}%", end=" " * 20)
            assembly.motor.forward(i)
            curr = assembly.ina226.current
            sleep(0.5)
            adjusted_field = blocking_get_mag_field(UART)
            measurements[plane]["curr"].append(curr)
            measurements[plane]["magfield"].append(adjusted_field[plane])

        assembly.motor.stop()

    x_currs = np.array(measurements["x"]["curr"])
    y_currs = np.array(measurements["y"]["curr"])
    z_currs = np.array(measurements["z"]["curr"])

    x_fields = np.array(measurements["x"]["magfield"])
    y_fields = np.array(measurements["y"]["magfield"])
    z_fields = np.array(measurements["z"]["magfield"])

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


SLOPES_AND_INTERCEPTS = {  # Defaults are derived from previous runs. Don't rely on them.
    "x": {"slope": 1136, "intercept": -125},
    "y": {"slope": 1091, "intercept": -1},
    "z": {"slope": 924, "intercept": -5},
}


def generate_field():
    print("Enter desired field:")

    x = input("x (mG): ")
    y = input("y (mG): ")
    z = input("z (mG): ")

    def get_p_control(desired_field):
        """
        Use the regression from calibration to calculate a control value.
        This control value is the difference between the target current and the actual current
        multiplied by the gain value constant PROP_GAIN, and intended to be used to adjust
        the duty cycle the motor drivers are currently being PWM'd at.
        """
        plane_controls = {"x": 0, "y": 0, "z": 0}

        for plane, assembly in MOTOR_ASSEMBLIES.items():
            slope = SLOPES_AND_INTERCEPTS[plane]["slope"]
            intercept = SLOPES_AND_INTERCEPTS[plane]["intercept"]
            # Invert equation:
            # field = slope * amps + intercept -> (field - intercept) / slope = amps
            target_curr = (desired_field[plane] - intercept) / slope
            process_curr = assembly.ina226.current
            err = abs(target_curr) - abs(process_curr)
            control_output = PROP_GAIN * err

            print(f'target: {target_curr} err: {err} control_output: {control_output}')

            plane_controls[plane] = control_output

        return plane_controls, target_curr

    try:
        desired_field = {
            "x": float(x),
            "y": float(y),
            "z": float(z),
        }

        prev_duty_cycles = {"x": 0, "y": 0, "z": 0}

        LOGGER.info("Generating: %s", desired_field)
        while True:
            try:
                plane_controls, target_curr = get_p_control(desired_field)

                for plane, assembly in MOTOR_ASSEMBLIES.items():
                    plane_ctrl = plane_controls[plane]
                    duty_cycle = prev_duty_cycles[plane] + int(plane_ctrl)
                    duty_cycle = max(0, min(100, duty_cycle))

                    if target_curr > 0:
                        assembly.motor.forward(duty_cycle)
                    else:
                        assembly.motor.reverse(duty_cycle)

                    prev_duty_cycles[plane] = duty_cycle

                sleep(0.5)

            except KeyboardInterrupt:
                for assembly in MOTOR_ASSEMBLIES.values():
                    assembly.motor.stop()
                break

    except TypeError as e:
        LOGGER.error(e)


def set_dc():
    try:
        field = str(input("Field (x, y, z): "))
        dc = int(input("Duty Cycle: "))
        direction = str(input("Direction (fwd, rev): "))
    except TypeError:
        LOGGER.error("Incorrect data type")
        return 0

    try:
        motor = MOTOR_ASSEMBLIES[field].motor
        ina226 = MOTOR_ASSEMBLIES[field].ina226
    except KeyError:
        LOGGER.error("Invalid field")
        return 0

    if not (0 < dc < 101):
        LOGGER.error("Duty cycle out of bounds")
        return 0

    if direction in ["forward", "f", "fwd"]:
        motor.forward(dc)
    elif direction in ["reverse", "r", "rev"]:
        motor.reverse(dc)
    else:
        LOGGER.error("Invalid direction")
        return 0

    try:
        while True:
            print(f"{ina226.current}A")
            sleep(1)

    except KeyboardInterrupt:
        LOGGER.info("Stopping")
        motor.stop()


def print_help():
    print(
        "Available commands:\n\r\
        help: print this message\n\r\
        calibrate: run a calibration sweep\n\r\
        field: create the desired field inside the cage\n\r\
        dcicsv: generate a csv of duty cycle to current values\n\r\
        fieldscsv: generate a csv of magfield readings over time\n\r\
        currmagcsv: print a csv of current to magnetic field measurements\n\r\
        slopes: print the current calibration values\n\r\
        setgain: set the PROP_GAIN constant. Don't change this if you don't know what it does.\n\r\
        magfield: continuously print the readings from the serial bridge once per second.\n\r\
        setdc: pwm a motor driver with a duty cycle and read its output current\r\n\
        "
    )


LOGGER.info("Entering main loop")
while True:
    action = input("> ")
    if action == "help":
        print_help()
    elif action == "calibrate":
        SLOPES_AND_INTERCEPTS = run_calibration_sweep()
    elif action == "dcicsv":
        plane = input("Plane (x, y, z): ")
        if plane not in ["x", "y", "z"]:
            LOGGER.error("Invalid plane. Choose x, y, or z")
            continue
        print_dci_csv(plane, MOTOR_ASSEMBLIES)
    elif action == "fieldscsv":
        try:
            time_str = input("Time(s): ")
            time = int(time_str)
            print_fields_csv(time, UART)
        except TypeError as e:
            print(e)
            continue
    elif action == "currmagcsv":
        print_curr_mag_csv(LOGGER, MOTOR_ASSEMBLIES, UART)
    elif action == "field":
        generate_field()
    elif action == "slopes":
        print(SLOPES_AND_INTERCEPTS)
    elif action == "setgain":
        gain = input("Gain: ")
        try:
            gain = int(gain)
            PROP_GAIN = gain
        except TypeError:
            print("Invalid type for PROP_GAIN - Must be an integer")
    elif action == "setdc":
        set_dc()
    elif action == "magfield":
        while True:
            try:
                print(blocking_get_mag_field(UART))
                sleep(1)
            except KeyboardInterrupt:
                continue
    else:
        print("Unsupported action. Please try again")
