from zxy6005s import ZXY6005s

psu = ZXY6005s("/dev/ttyUSB0")
psu.connec()

psu.set_voltage(4.0)
psu.set_current(0.5)

psu.enable_output()
time.sleep(10)
psu.disable_output()

psu.disconnect()
