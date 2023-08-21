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
            print(self.psu.model(arg[0].upper()))
    
    #Help message for model command.
    def help_model(self):
        print("Device name can be 'X', 'Y' or 'Z'. ")
    
    #Takes device name and returns firmware version.
    def do_firmware(self, arg):
        if not self.mock:
            print(self.psu.firmware_version(arg[0].upper()))
    
    #Help message for firmware function.
    def help_firmware(self):
        print("Device name can be 'X', 'Y', or 'Z'. ")
    
    #Turns on specified power supply.     
    def do_power(self, arg):
        if not self.mock:
            args = arg.split(" ")
            print(self.psu.set_output(args[0].upper(), args[1]=="1"))
         
    #Power supply on/off help message.
    def help_power(self):
        print("Power <mag> <value>. ")
        print("Device name can be 'X', 'Y', or 'Z'. ")
        print("Value can be '1' or '0', where '1' is on and '0' is off.")
    
    #Sets amp hour to counter value give. Takes device name and int value.
    def do_amp_hour(self, arg):
        if not self.mock:
            print(self.psu.set_amp_hour(arg[0].upper(), arg[1]))
    
    #Amp hour set function help message.
    def help_amp_hour(self):
        print("Please enter device name and integer")
        print("Device name can be 'X', 'Y', or 'Z'. ")
        print("Value needs to be in amps")
    
    #Returns amp hour of a given device.
    def do_return_amp_hour(self, arg):
        if not self.mock:
            print(self.psu.return_amp_hour(arg[0].upper()))
    
    #Help message for return amp hour
    def help_return_amp_hour(self):
        print("Device name can be 'X', 'Y', or 'Z'. ")
        print("This function will return amp hour of device name given.")
    
    #Setting voltage for a specified device.    
    def do_voltage(self, arg):
        args = arg.split(" ")
        try: 
            value = int(args[1])
        except ValueError:
            self.help_voltage()
            return
        if not self.mock:
            self.psu.set_voltage(arg[0].upper(), value)
    
    #Help message for set voltage.
    def help_voltage(self):
        print("Device name can be 'X', 'Y', or 'Z'. ")
        print("This function requires a int value. Please input voltage desired as an integer. ")
    
    #Returns voltage of a given device.     
    def do_return_voltage(self, arg):
        if not self.mock:
            print(self.psu.return_voltage(arg[0].upper()))
    
    #Help message for returning voltage.
    def help_return_voltage(self):
        print("Device name can be 'X', 'Y', or 'Z'. ")
        print("This function is meant to return voltage of a given device. ")  
    
    #Sets current limit to be a value entered.
    def do_current_limit(self, arg):
        args = arg.split(" ")
        try: 
            value = int(args[1])
        except ValueError:
            self.help_current_limit()
            return
        if not self.mock:
            print(self.psu.set_current_limit(arg[0].upper(), value))
    
    #Help message for current_limit function.
    def help_current_limit(self):
        print("Device name can only be 'X', 'Y' or 'Z'. ")
        print("Value must be a integer with voltage units. ")
        print("This function takes a device name and value and sets the current limit to that value. ")
    
    #Takes a device name and returns its current in amps.   
    def do_return_current(self, arg):
        if not self.mock:
            print(self.psu.return_current(arg[0].upper()))
    
    #Help message for returning current function.
    def help_return_current(self):
        print("This function takes a device name and returns its current in amps. ")
        print("Device name can be 'X', 'Y', or 'Z'. ")
    
    #Returns the mode of a given device.
    def do_return_mode(self, arg):
        if not self.mock:
            print(self.psu.return_mode(arg[0].upper()))
    
    #Help message for return_mode function.
    def help_return_mode(self):
        print("This function takes a device name and returns what mode it is in. ")
        print("Modes can be CV (Constant Voltage) or CC (Constant Current). ")
        print("Device name can only be 'X', 'Y', 'Z'. ")
    
    #Returns the temperature of a device in Celsius.   
    def do_return_temp(self, arg):
        if not self.mock:
            print(self.psu.return_temp(arg[0].upper()))
    
    #Help message for return_temp function.
    def help_return_temp(self):
        print("This function returns the temperature of a device name in Celsius. ")
        print("Device name can only be 'X', 'Y', or 'Z'. ")
    
    #Set X H-bridge to positive polarity. 
    def do_set_positive_X(self, arg):
        if not self.mock:
            print(self.arduino.set_positive_X())
    
    #Help message for positive_X
    def help_set_positive_X(self):
        print("This function sets the X bridge to positive polarity.")
        print("Accepted values are 'x'. ")
    
    #Set Y H-bridge to positive polarity.
    def do_set_positive_Y(self, arg):
        if not self.mock:
            print(self.arduino.set_positive_Y())
    
    #Help message for positive_Y. 
    def help_set_positive_Y(self):
        print("This function sets the Y bridge to positive polarity. ")
        print("Accepted values are 'y'. ")
    
    #Set Z H-bridge to positive polarity.        
    def do_set_positive_Z(self, arg):
        if not self.mock:
            print(self.arduino.set_positive_Z())
    
    #Help message for positive_Z. 
    def help_set_positive_Z(self):
        print("This function sets the Z bridge to positive polarity. ")
        print("Accepted values are: 'z'. ")
    
    #Set X H-bridge to negative polarity.
    def do_set_negative_X(self, arg):
        if not self.mock:
            print(self.arduino.set_negative_X())
    
    #Help message for positive_x.
    def help_set_negative_X(self):
        print("This function sets the X H-bridge to negative polarity.")
        print("Accepted values are: 'X'. ")
    
    #Set Y H-bridge to negative polarity.    
    def do_set_negative_Y(self, arg):
        if not self.mock:
            print(self.arduino.set_negative_Y())
    
    #Help message for negative_Y.
    def help_set_negative_Y(self):
        print("This function sets the Y H-bridge to negative polarity. ")
        print("Accepted values are: 'Y'. ")
    
    #Set Z H-bridge to negative polarity.    
    def do_set_negative_Z(self, arg):
        if not self.mock:
            print(self.arduino.set_negative_Z())
    
    #Help message for set_negative_Z.
    def help_set_negative_Z(self):
        print("This function sets the Z H-bridge to negative polarity. ")
        print("Accepted values are: 'Z'. ")
    
    #Deactivates all H-bridges. 
    def do_deactivate_all(self, arg):
        if not self.mock:
            self.arduino.deactivate_all()
    
    #Help message for deactivate_all.
    def help_deactivate_all(self):
        print("This function deactivates all H-Bridges. ")
        print("Accepted values are: 'a'. ")
    
    #Deactivates the X H-bridge.    
    def do_deactivate_X(self, arg):
        if not self.mock:
            self.arduino.deactivate_X()
    
    #Help message for deactivate_X.         
    def help_deactivate_X(self):
        print("This function deactivates just the X H-bridge. ")
        print("Accepted values are: 'b'. ")
    
    #Deactivates the Y H-bridge.    
    def do_deactivate_Y(self, arg): 
        if not self.mock: 
            self.arduino.deactivate_Y()
    
    #Help message for deactivate_Y. 
    def help_deactivate_Y(self):
        print("This function deactivates just the Y H-bridge.")
        print("Accepted values are: 'c'. ")
    
    #Deactivates the Z H-bridge. 
    def do_deactivate_Z(self, arg): 
        if not self.mock:
            self.arduino.deactivate_Z()
    
    #Help message for deactivate_Z.         
    def help_deactivate_Z(self): 
        print("This function deactivates just the Z H-bridge. ")
        print("Accepted values are: 'd'. ")
    
    #Returns the magnetic field reading. 
    def do_magnetometer_reading(self, arg):
        if not self.mock:
            print(self.arduino.get_magnetometer_reading())
    
    #Help message for magnetometer_reading.
    def help_magnetometer_reading(self):
        print("This function returns the current magnetic field reading. ")
        print("Accepted values are: 'm'. ")
    
    #Is the magnetometer on or off?    
    def do_magnetometer_status(self, arg):
        if not self.mock:
            print(self.arduino.get_magnetometer_status())
    
    #Help message for magnetometer_status. 
    def help_magnetometer_status(self):
        print("This function returns whether the magnetometer is on/off. ")
        print("Accepted values are: 'q'. ")
    
    #Returns the status of all 3 H-bridges.     
    def do_bridge_status(self, arg):
        if not self.mock:
            print(self.arduino.get_bridge_status())
    
    #Help message for bridge_status. 
    def help_bridge_status(self):
        print("This function returns the status of all 3 H-bridges. ")
        print("1 = Bridge set to positive polarity. ")
        print("2 = Bridge set to negative polarity. ")
        print("0 = Bridge is turned off. ")
        print("Accepted values are: 's'. ")
    
    #Returns the temperature of the magnetometer. 
    def do_magnetometer_temp(self, arg):
        if not self.mock:
            print(self.arduino.get_magnetometer_temp())
    
    #Help message for magnetometer_temp. 
    def help_magnetometer_temp(self):
        print("This function returns the temperature of the magnetometer in Celsius. ")
        print("Accepted values are: 't'. ")
            
    
    #Closes program and exits. 
    def do_exit(self, arg):
        print("Disabling power supplies.")
        self.psu.set_output('X', 0)
        self.psu.set_output('Y', 0)
        self.psu.set_output('Z', 0)
        return True
    #Help message for exit program.
    def help_exit(self):
        print("Type in exit to close the program ")

def main():
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
    shell.cmdloop()

if __name__ == "__main__":
    main()
