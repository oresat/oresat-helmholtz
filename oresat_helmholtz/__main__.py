import cmd
from argparse import ArgumentParser

from .Arduino import Arduino, ArduinoCommands
from .ZXY6005s import ZXY6005s, ZXY6005sCommands

class HelmholtzShell(cmd.Cmd):
    intro = "Welcome to the Helmholtz Shell! Type 'help' to list commands \n"
    prompt = "> "
    file = None
    
    #Main objection construction for power supply and arduino libraries.
    def __init__(self, arduino: Arduino, psu: ZXY6005s, mock:bool):
        super().__init__()
        self.arduino = arduino
        self.psu = psu
        self.mock = mock
    
    #Takes device name and returns model.
    def do_model(self, arg):
        if not self.mock:
            self.psu.model(arg[0].upper())
    
    #Help message for model command.
    def help_model(self):
        print("Device name can be 'X', 'Y' or 'Z'. ")
    
    #Takes device name and returns firmware version.
    def do_firmware(self, arg):
        if not self.mock:
            self.psu.firmware_version(arg[0].upper())
    
    #Help message for firmware function.
    def help_firmware(self):
        print("Device name can be 'X', 'Y', or 'Z'. ")
    
    #Turns on specified power supply.     
    def do_power(self, arg):
        if not self.mock:
            self.psu.set_output(arg[0].upper(), arg[1]=="1")
         
    #Power supply on/off help message.
    def help_power(self):
        print("Power <mag> <value>. ")
        print("Device name can be 'X', 'Y', or 'Z'. ")
        print("Value can be '1' or '0', where '1' is on and '0' is off.")
    
    #Closes program and exits. 
    def do_exit(self, arg):
        return True
    #Help message for exit program.
    def help_exit(self):
        print("Type in exit to close the program ")

def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--device', default = '/dev/ttyUSB3', help='path to arduino device')
    parser.add_argument('-m', '--mock', action = "store_true")
    args = parser.parse_args()
    
    if args.mock:
        arduino = None
        psu = None
    else:
        arduino = Arduino(args.device)
        psu = ZXY6005s()
    
    
    shell = HelmholtzShell(arduino, psu, args.mock)
    shell.cmdloop()

if __name__ == "__main__":
    main()
