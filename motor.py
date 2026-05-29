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
