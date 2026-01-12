from time import sleep

import board
from digitalio import DigitalInOut, Direction

LED_0 = DigitalInOut(board.LED)
LED_0.direction = Direction.OUTPUT


def blink_led():
    # blinks LED on Pico once a second
    LED_0.value = True
    sleep(0.5)
    LED_0.value = False
    sleep(0.5)
