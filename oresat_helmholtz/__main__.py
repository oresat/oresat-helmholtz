import cmd
from argparse import ArgumentParser

from .Arduino import Arduino, ArduinoCommands
from .ZXY6005s import ZXY6005s, ZXY6005sCommands

class HelmholtzShell(cmd.Cmd):
    intro = "Welcome to the Helmholtz Shell! Type 'help' to list commands \n"
    prompt = "> "
    file = None
    
    def __init__(self, arduino: Arduino, psu: ZXY6005s, mock:bool):
        super().__init__()
        self.arduino = arduino
        self.psu = psu
        self.mock = mock
        
    def do_power(self, arg):
        if not self.mock:
            self.psu.set_output(arg[0].upper(), arg[1]=="1")
         

    def help_power(self):
        print("power <mag> <value> ")
        print("mag can be 'X', 'Y', or 'Z")
        print("value can be '1' or '0'")
    
    def do_exit(self, arg):
        return True
    
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
