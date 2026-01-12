import adafruit_logging as logging
import board
from digitalio import DigitalInOut, Direction

from blink import blink_led

logger = logging.getLogger('Helmholtz logger')
logger.setLevel(logging.DEBUG)

logger.info("Oresat Helmholtz Cage Firmware v2")

LED_0 = DigitalInOut(board.LED)
LED_0.direction = Direction.OUTPUT

LED_1 = DigitalInOut(board.GP13)
LED_1.direction = Direction.OUTPUT

LED_2 = DigitalInOut(board.GP14)
LED_2.direction = Direction.OUTPUT

LED_3 = DigitalInOut(board.GP15)
LED_3.direction = Direction.OUTPUT

# X axis pins
X_IN1 = DigitalInOut(board.GP2)
X_IN1.direction = Direction.OUTPUT
X_IN2 = DigitalInOut(board.GP3)
X_IN2.direction = Direction.OUTPUT

# Y axis pins
Y_IN1 = DigitalInOut(board.GP6)
Y_IN1.direction = Direction.OUTPUT
Y_IN2 = DigitalInOut(board.GP7)
Y_IN2.direction = Direction.OUTPUT

# Z axis pins
Z_IN1 = DigitalInOut(board.GP10)
Z_IN1.direction = Direction.OUTPUT
Z_IN2 = DigitalInOut(board.GP11)
Z_IN2.direction = Direction.OUTPUT

while True:
    blink_led(LED_0, 0.5)


# Motor H-Bridge controls
# Use these functions to determine the direction of current
# motorStop(IN1, IN2):
#     IN1.value = False
#     IN2.value = False
#
# motorForward(IN1, IN2):
#     IN1.value = True
#     IN2.value = False
#
# motorReverse(IN1, IN2):
#     IN1.value = False
#     IN2.value = True
#
# motorBrake(IN1, IN2):
#     IN1.value = True
#     IN2.value = True
#
# # Set test directions
# motorStop(X_IN1, X_IN2)
# motorForward(Y_IN1, Y_IN2)
# motorStop(Z_IN1, Z_IN2)
