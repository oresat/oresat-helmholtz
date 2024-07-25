from helmholtzcage import Arduino, HelmholtzShell, ZXY6005s
from argparse import ArgumentParser

#Main program. Objects declared here. Shell built. 
parser = ArgumentParser()
parser.add_argument('-l', '--arduino-location', help='Location to Arduino. ')
parser.add_argument('-m', '--mock', action = "store_true")
args = parser.parse_args()

if args.mock:
    arduino = None
    psu = None
else:
    arduino = Arduino(args.arduino_location)
    psu = ZXY6005s()

shell = HelmholtzShell(arduino, psu, args.mock)
for i in 'xyz':
    shell.do_voltage(i + " 700")
    shell.do_current_limit(i + " 1000")
shell.cmdloop()

