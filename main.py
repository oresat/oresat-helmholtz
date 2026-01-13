from time import sleep

import board
from digitalio import DigitalInOut, Direction

import adafruit_logging as logging
from motor import Motor

logger = logging.getLogger('Helmholtz logger')
logger.setLevel(logging.DEBUG)

logger.info("Oresat Helmholtz Cage Firmware v2")

PICO_LED = DigitalInOut(board.LED)
PICO_LED.direction = Direction.OUTPUT

motor_x = Motor(in1=board.GP2, in2=board.GP3, led=board.GP13)
motor_y = Motor(in1=board.GP6, in2=board.GP7, led=board.GP14)
motor_z = Motor(in1=board.GP10, in2=board.GP11, led=board.GP15)

while True:
    PICO_LED.value = True
    sleep(1)
    PICO_LED.value = False
    motor_x.forward()
    sleep(1)
    motor_x.stop()
    motor_y.reverse()
    sleep(1)
    motor_y.stop()
    motor_z.reverse()
    sleep(1)
    motor_z.stop()
