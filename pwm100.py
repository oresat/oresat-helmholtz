import time

from machine import I2C, Pin

import ina226

# Keep Pins static (100% duty cycle)
p3 = Pin(3, Pin.OUT)
p2 = Pin(2, Pin.OUT)

# setup I2C
i2c = I2C(scl=Pin(1), sda=Pin(0))

ina = ina226.INA226(i2c, 0x40)
ina.set_calibration()

p3.off()
p2.on()

while True:
    print(f'Vbus   = {ina.bus_voltage}')
    print(f'Vshunt = {ina.shunt_voltage}')
    print(f'Ishunt = {ina.current}')
    print(f'Power  = {ina.power}')
    print()

    p2.toggle()
    p3.toggle()
    time.sleep(1)
