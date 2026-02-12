from digitalio import DigitalInOut, Direction
from pwmio import PWMOut


class Motor:
    def __init__(self, in1, in2, led):
        """
        Initialize motor with GPIO pins and DAC.

        Args:
            in1: GPIO output pin for in1
            in2: GPIO output pin for in2
        """
        self.in1 = PWMOut(in1, frequency=100, duty_cycle=0)
        self.in2 = PWMOut(in2, frequency=100, duty_cycle=0)
        self.led = DigitalInOut(led)
        self.led.direction = Direction.OUTPUT

    def stop(self):
        self.led.value = False
        self.in1.duty_cycle = 0
        self.in2.duty_cycle = 0

    def forward(self, percent_multiplier):
        self.led.value = True
        self.in1.duty_cycle = int(2**16 * (percent_multiplier * 0.01))
        self.in2.duty_cycle = 0

    def reverse(self, percent_multiplier):
        self.led.value = True
        self.in1.duty_cycle = 0
        self.in2.duty_cycle = int(2**16 * (percent_multiplier * 0.01))

    def brake(self):
        self.led.value = False
        self.in1.duty_cycle = 2**16
        self.in2.duty_cycle = 2**16
