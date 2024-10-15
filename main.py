from helmholtzcage import Arduino, HelmholtzShell, ZXY6005s, Magnetometer, utils
from argparse import ArgumentParser

#Main program. Objects declared here. Shell built. 
parser = ArgumentParser()
parser.add_argument('-l', '--arduino-location', default='1-1.2.2', help='Location of Arduino. ')
parser.add_argument('-s', '--meter-location', default='1-1.2.3', help='Location of Meter.')
parser.add_argument('-x', '--x-location', default='1-1.2.4.3', help='Location of x-axis controller')
parser.add_argument('-y', '--y-location', default='1-1.2.4.2', help='Location of y-axis controller')
parser.add_argument('-z', '--z-location', default='1-1.2.4.1', help='Location of z-axis controller')
parser.add_argument('-d', '--debug-port', help='Debug serial port')
parser.add_argument('-m', '--mock', action = "store_true")
args = parser.parse_args()

if args.mock:
    arduino = None
    psu = None
    meter = None
    utility = None
else:
    arduino = Arduino(args.debug_port if args.debug_port else args.arduino_location)
    psX = ZXY6005s(args.x_location, args.debug_port)
    psY = ZXY6005s(args.y_location, args.debug_port)
    psZ = ZXY6005s(args.z_location, args.debug_port)
    meter = Magnetometer.Magnetometer(args.meter_location, args.debug_port)
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

