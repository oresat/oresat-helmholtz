import sys

import board
from busio import I2C, UART
from cli import Cli, Command
from data import print_curr_mag_csv, print_dci_csv, print_fields_csv
from ina226 import INA226
from magfield import generate_field, run_calibration_sweep
from motor import Motor, set_dc, stop_all_motor_drivers
from uart import print_bridge_vals

import adafruit_logging as logging

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


class CageState:
    def __init__(self):
        # Defaults are derived from previous runs. Don't rely on them.
        self.slopes_and_intercepts = {
            "x": {"slope": 1136, "intercept": -125},
            "y": {"slope": 1091, "intercept": -1},
            "z": {"slope": 924, "intercept": -5},
        }

    def print_slopes_and_intercepts(self):
        "CLI callback to print the current calibration values"
        sys.stdout.write(f"{self.slopes_and_intercepts}\n")


class MotorDriverAssembly:
    """
    Container to hold a coil's motor driver and ina226
    """

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


STATE = CageState()

# run_calibration_sweep(STATE)

cli = Cli(prompt="> ")

cli.register_commands(
    [
        Command(
            name="calibrate",
            callback=run_calibration_sweep,
            default_args=[STATE, MOTOR_ASSEMBLIES, UART],
            argspec=None,
            help_text="Run a calibration sweep",
        ),
        Command(
            name="field",
            callback=generate_field,
            default_args=[STATE, MOTOR_ASSEMBLIES],
            argspec=[(("-x",), float), (("-y",), float), (("-z",), float)],
            help_text=(
                "Create the desired field inside the cage.\n"
                "For negative values, wrap the number in quotes."
            ),
        ),
        Command(
            name="dcicsv",
            callback=print_dci_csv,
            default_args=[MOTOR_ASSEMBLIES],
            argspec=[(("-p", "-plane"), str)],
            help_text="Generate a csv of duty cycle to current values",
        ),
        Command(
            name="fieldcsv",
            callback=print_fields_csv,
            default_args=[UART],
            argspec=[(("-t", "-time"), int)],
            help_text="Generate a csv of magfield readings over time (seconds)",
        ),
        Command(
            name="currmagcsv",
            callback=print_curr_mag_csv,
            default_args=[MOTOR_ASSEMBLIES, UART],
            argspec=None,
            help_text="Print a csv of current to magnetic field measurements",
        ),
        Command(
            name="calvals",
            callback=STATE.print_slopes_and_intercepts,
            default_args=None,
            argspec=None,
            help_text="Print the current calibration values",
        ),
        Command(
            name="bridgevals",
            callback=print_bridge_vals,
            default_args=[UART],
            argspec=None,
            help_text="Continuously print the readings from the serial bridge once per second",
        ),
        Command(
            name="setdc",
            callback=set_dc,
            default_args=[MOTOR_ASSEMBLIES],
            argspec=[
                (("-p", "-plane"), str),
                (("-d", "-direction"), str),
                (("-dc", "-dutycycle"), int),
            ],
            help_text="Pwm a motor driver with a duty cycle and read its output current",
        ),
        Command(
            name="stop",
            callback=stop_all_motor_drivers,
            default_args=[MOTOR_ASSEMBLIES],
            argspec=None,
            help_text="Stop all motor drivers",
        ),
    ]
)
LOGGER.info("CLI Initialized")

LOGGER.info("Entering main loop")
while True:
    if cli.repl() == "exit":
        break
