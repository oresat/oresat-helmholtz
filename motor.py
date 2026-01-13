from digitalio import DigitalInOut, Direction


class Motor:
    def __init__(self, in1, in2, led):
        """
        Initialize motor with GPIO pins and DAC.

        Args:
            in1: GPIO output pin for in1
            in2: GPIO output pin for in2
            ps: GPIO output pin for power save
        """
        self.in1 = DigitalInOut(in1)
        self.in1.direction = Direction.OUTPUT
        self.in2 = DigitalInOut(in2)
        self.in2.direction = Direction.OUTPUT
        self.led = DigitalInOut(led)
        self.led.direction = Direction.OUTPUT

    def stop(self):
        self.led.value = False
        self.in1.value = False
        self.in2.value = False

    def forward(self):
        self.led.value = True
        self.in1.value = True
        self.in2.value = False

    def reverse(self):
        self.led.value = True
        self.in1.value = False
        self.in2.value = True

    def brake(self):
        self.led.value = False
        self.in1.value = True
        self.in2.value = True
