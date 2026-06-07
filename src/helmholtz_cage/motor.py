import sys
from time import sleep

from digitalio import DigitalInOut, Direction
from pwmio import PWMOut

MAX_DC = 65535  # 2**16 - 1
PWM_FREQ = 12500  # min pulse width = 800ns, 0.01 [1%] * (1 / 12.5k) = 800ns


class Motor:
    def __init__(self, in1, in2, led):
        """
        Initialize motor with GPIO pins and DAC.

        Args:
            in1: GPIO output pin for in1
            in2: GPIO output pin for in2
        """
        self.in1 = PWMOut(in1, frequency=PWM_FREQ, duty_cycle=0)
        self.in2 = PWMOut(in2, frequency=PWM_FREQ, duty_cycle=0)
        self.led = DigitalInOut(led)
        self.led.direction = Direction.OUTPUT

    def stop(self):
        self.led.value = False
        self.in1.duty_cycle = 0
        self.in2.duty_cycle = 0

    def forward(self, duty_cycle_percent):
        dc = 100 - duty_cycle_percent
        self.led.value = True
        self.in1.duty_cycle = MAX_DC
        self.in2.duty_cycle = int(MAX_DC * (dc * 0.01))

    def reverse(self, duty_cycle_percent):
        dc = 100 - duty_cycle_percent
        self.led.value = True
        self.in1.duty_cycle = int(MAX_DC * (dc * 0.01))
        self.in2.duty_cycle = MAX_DC

    def brake(self):
        self.led.value = False
        self.in1.duty_cycle = MAX_DC
        self.in2.duty_cycle = MAX_DC


def set_dc(motor_assemblies, plane, direction, duty_cycle):
    """
    CLI callback to the duty cycle on a specific motor driver
    and read the current it outputs in a loop
    """
    try:
        motor = motor_assemblies[plane].motor
        ina226 = motor_assemblies[plane].ina226
    except KeyError:
        return "Invalid plane\r\n"

    if not (-1 < duty_cycle < 101):
        return "Duty cycle out of bounds\r\n"

    if direction in ["forward", "f", "fwd"]:
        motor.forward(duty_cycle)
    elif direction in ["reverse", "r", "rev"]:
        motor.reverse(duty_cycle)
    else:
        return "Invalid direction\r\n"

    try:
        sys.stdout.write("\n")
        while True:
            sys.stdout.write(f"{ina226.current}A\n")
            sleep(1)

    except KeyboardInterrupt:
        motor.stop()


def stop_all_motor_drivers(motor_assemblies):
    """
    CLI callback to stop all motor drivers
    """
    for assembly in motor_assemblies.values():
        assembly.motor.stop()
    return ""
