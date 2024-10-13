from helmholtzcage import Arduino, HelmholtzShell, ZXY6005s, Magnetometer, utils
from argparse import ArgumentParser

#Main program. Objects declared here. Shell built. 
parser = ArgumentParser()
parser.add_argument('-l', '--arduino-location', help='Location to Arduino. ') #1-1.2.2
parser.add_argument('-s', '--meter-location', help='Location to Meter.') #1-1.2.3
parser.add_argument('-m', '--mock', action = "store_true")
args = parser.parse_args()

if args.mock:
    arduino = None
    psu = None
    meter = None
    utility = None
else:
    arduino = Arduino(args.arduino_location)
    psX = ZXY6005s('1-1.2.4.3', '/dev/pts/4')
    psY = ZXY6005s('1-1.2.4.2', '/dev/pts/4')
    psZ = ZXY6005s('1-1.2.4.1', '/dev/pts/4')
    meter = Magnetometer.Magnetometer(args.meter_location, '/dev/pts/4')
    utility = utils.Utilities(meter=meter, arduino=arduino, psu=(psX, psY, psZ))

shell = HelmholtzShell(arduino, (psX, psY, psZ), meter, utility, args.mock)

def set_all(mV, mA, power):
    for device in 'XYZ':
        shell.do_voltage(f"{device} {mV}")
        shell.do_current_limit(f"{device} {mA}")
        shell.do_power(f"{device} {power}")

set_all(700, 500, 1)
try:
    shell.cmdloop()
finally:
    set_all(0, 0, 0)

