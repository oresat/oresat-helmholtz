from machine import I2C, PWM, Pin

import ina226

# Fast Decay PWM Mode
# toggles both Pins at same time (one is inverted)

# initialize PWM on GPIO2
pwm_a = PWM(Pin(2), freq=50000)
pwm_b = PWM(Pin(3), freq=50000, invert=True)  # On the same slice as Pin2

# setup I2C
i2c = I2C(scl=Pin(1), sda=Pin(0))

ina = ina226.INA226(i2c, 0x40)
ina.set_calibration()

duty_per = 80
duty_u16 = round(duty_per / 100 * 65536)
pwm_a.duty_u16(duty_u16)  # duty cycle
pwm_b.duty_u16(duty_u16)

print(ina.bus_voltage)
print(ina.shunt_voltage)
print(ina.current)
print(ina.power)
