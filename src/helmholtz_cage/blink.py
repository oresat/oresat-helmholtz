from time import sleep

import board
from digitalio import DigitalInOut, Direction

PICO_LED = DigitalInOut(board.LED)
PICO_LED.direction = Direction.OUTPUT


def blink_led(led, interval: float):
    """Blink an led on a given interval"""
    led.value = True
    sleep(interval)
    led.value = False
    sleep(interval)
