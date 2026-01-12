from time import sleep


def blink_led(led, interval: float):
    """Blink an led on a given interval"""
    led.value = True
    sleep(interval)
    led.value = False
    sleep(interval)
