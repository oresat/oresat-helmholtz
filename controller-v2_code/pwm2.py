from machine import Pin, PWM
import time
import ina226
from machine import Pin, I2C

# PWM Slow Decay mode
pwm_a = PWM(Pin(3), freq=50000)  	# initialize PWM on GPIO3
p2 = Pin(2, Pin.OUT)				# Keep Pin 2 H

# setup I2C
i2c = I2C(scl=Pin(1), sda=Pin(0))

ina = ina226.INA226(i2c, 0x40)
ina.set_calibration()

p2.on()			# set Pin 2 to H
duty_per = 20
duty_u16 = round(duty_per/100 * 65536)
pwm_a.duty_u16(duty_u16) # duty cycle

print(ina.bus_voltage)
print(ina.shunt_voltage)
print(ina.current)
print(ina.power)


