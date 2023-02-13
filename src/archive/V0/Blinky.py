#!/usr/bin/env python

# Bliss 5-9-18
# Fun with LED and PI
# POWER TO FUCKING RESISTOR TO FUCKING LONG LEG
# SHORT LEG TO GROUND FFS

print "Hello"
import time
import RPi.GPIO as GPIO
raw_input()

#gpio = GPIO.get_platform_gpio()
#GPIO.setwarnings(True)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, True)
GPIO.output(23, False)
led_pin=23
#GPIO.setup(led_pin.GPIO.OUT)
try:
	while True:
		GPIO.output(led_pin, True)
		time.sleep(0.5)
		GPIO.output(led_pin, False)
		time.sleep(0.5)
		raw_input()
finally:
	print "Cleaning..."
	GPIO.cleanup()
