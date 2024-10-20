import cmd
import csv
from argparse import ArgumentParser

from .Arduino import Arduino, ArduinoCommands
from .ZXY6005s import ZXY6005s, ZXY6005sCommands
from .Magnetometer import Magnetometer, MagnetometerCommands
from .utils import Utilities

class HelmholtzShell(cmd.Cmd):
    intro = "Welcome to the Helmholtz Cage Shell! Type 'help' to list commands \n"
    prompt = "> "
    file = None
    
    #Main objection construction for power supply and arduino libraries.
    def __init__(self, arduino: Arduino, psu: ZXY6005s, meter: Magnetometer, utility: Utilities, mock:bool):
        super().__init__()
        self.arduino = arduino
        self.mock = mock
        self.meter = meter
        self.utility = utility
        self.psu = {}
        for axis, power_supply in zip('XYZ', psu):
            self.psu[axis] = power_supply
    
    #Takes device name and returns model.
    def do_model(self, arg):
        axis = arg.split(" ")[0]
        if not self.mock:
            print(self.psu[axis.upper()].model())
    
    #Help message for model command.
    def help_model(self):
        print("Prints the model of the power supply device.")
        print("Device name can be 'X', 'Y' or 'Z'. ")
    
    #Takes device name and returns firmware version.
    def do_firmware(self, axis):
        if not self.mock:
            print(self.psu[axis[0].upper()].firmware_version())
    
    #Help message for firmware function.
    def help_firmware(self):
        print("Device name can be 'X', 'Y', or 'Z'. ")
    
    #Turns on specified power supply.     
    def do_power(self, arg):
        if not self.mock:
            (axis, power) = arg.split(" ")
            print(self.psu[axis.upper()].set_output(power=="1"))
         
    #Power supply on/off help message.
    def help_power(self):
        print("Power <mag> <value>. ")
        print("Device name can be 'X', 'Y', or 'Z'. ")
        print("Value can be '1' or '0', where '1' is on and '0' is off.")
    
    #Sets amp hour to counter value give. Takes device name and int value.
    def do_amp_hour(self, arg):
        (axis, mAh) = arg.split(" ")
        if not self.mock:
            print(self.psu[axis.upper()].set_amp_hour(mAh))
    
    #Amp hour set function help message.
    def help_amp_hour(self):
        print("Please enter device name and integer")
        print("Device name can be 'X', 'Y', or 'Z'. ")
        print("Value needs to be in amps")
    
    #Returns amp hour of a given device.
    def do_return_amp_hour(self, axis):
        if not self.mock:
            print(self.psu[axis[0].upper()].return_amp_hour())
    
    #Help message for return amp hour
    def help_return_amp_hour(self):
        print("Device name can be 'X', 'Y', or 'Z'. ")
        print("This function will return amp hour of device name given.")
    
    #Setting voltage for a specified device.    
    def do_voltage(self, arg):
        try: 
            (axis, mV) = arg.split(" ")
        except ValueError:
            self.help_voltage()
            return
        if not self.mock:
            self.psu[axis].set_voltage(int(mV))
    
    #Help message for set voltage.
    def help_voltage(self):
        print("Device name can be 'X', 'Y', or 'Z'. ")
        print("This function requires a int value. Please input voltage desired as an integer. ")
    
    #Returns voltage of a given device.     
    def do_return_voltage(self, axis):
        if not self.mock:
            print(self.psu[axis[0].upper()].return_voltage())
    
    #Help message for returning voltage.
    def help_return_voltage(self):
        print("Device name can be 'X', 'Y', or 'Z'. ")
        print("This function is meant to return voltage of a given device. ")  
    
    #Sets current limit to be a value entered.
    def do_current_limit(self, arg):
        (axis, mA) = arg.split(" ")
        try: 
            value = int(mA)
        except ValueError:
            self.help_current_limit()
            return
        if not self.mock:
            print(self.psu[axis].set_current_limit(int(mA)))
    
    #Help message for current_limit function.
    def help_current_limit(self):
        print("Device name can only be 'X', 'Y' or 'Z'. ")
        print("Value must be a integer with voltage units. ")
        print("This function takes a device name and value and sets the current limit to that value. ")
    
    #Takes a device name and returns its current in amps.   
    def do_return_current(self, axis):
        if not self.mock:
            print(self.psu[axis[0].upper()].return_current())
    
    #Help message for returning current function.
    def help_return_current(self):
        print("This function takes a device name and returns its current in amps. ")
        print("Device name can be 'X', 'Y', or 'Z'. ")
    
    #Returns the mode of a given device.
    def do_return_mode(self, axis):
        if not self.mock:
            print(self.psu[axis[0].upper()].return_mode())
    
    #Help message for return_mode function.
    def help_return_mode(self):
        print("This function takes a device name and returns what mode it is in. ")
        print("Modes can be CV (Constant Voltage) or CC (Constant Current). ")
        print("Device name can only be 'X', 'Y', 'Z'. ")
    
    #Returns the temperature of a device in Celsius.   
    def do_return_temp(self, axis):
        if not self.mock:
            print(self.psu[axis[0].upper()].return_temp())
    
    #Help message for return_temp function.
    def help_return_temp(self):
        print("This function returns the temperature of a device name in Celsius. ")
        print("Device name can only be 'X', 'Y', or 'Z'. ")
    
    #Set X H-bridge to positive polarity. 
    def do_set_positive_X(self, _):
        if not self.mock:
            print(self.arduino.set_positive_X())
    
    #Help message for positive_X
    def help_set_positive_X(self):
        print("This function sets the X bridge to positive polarity.")
        print("Accepted values are 'x'. ")
    
    #Set Y H-bridge to positive polarity.
    def do_set_positive_Y(self, _):
        if not self.mock:
            print(self.arduino.set_positive_Y())
    
    #Help message for positive_Y. 
    def help_set_positive_Y(self):
        print("This function sets the Y bridge to positive polarity. ")
        print("Accepted values are 'y'. ")
    
    #Set Z H-bridge to positive polarity.        
    def do_set_positive_Z(self, _):
        if not self.mock:
            print(self.arduino.set_positive_Z())
    
    #Help message for positive_Z. 
    def help_set_positive_Z(self):
        print("This function sets the Z bridge to positive polarity. ")
        print("Accepted values are: 'z'. ")
    
    #Set X H-bridge to negative polarity.
    def do_set_negative_X(self, _):
        if not self.mock:
            print(self.arduino.set_negative_X())
    
    #Help message for positive_x.
    def help_set_negative_X(self):
        print("This function sets the X H-bridge to negative polarity.")
        print("Accepted values are: 'X'. ")
    
    #Set Y H-bridge to negative polarity.    
    def do_set_negative_Y(self, _):
        if not self.mock:
            print(self.arduino.set_negative_Y())
    
    #Help message for negative_Y.
    def help_set_negative_Y(self):
        print("This function sets the Y H-bridge to negative polarity. ")
        print("Accepted values are: 'Y'. ")
    
    #Set Z H-bridge to negative polarity.    
    def do_set_negative_Z(self, _):
        if not self.mock:
            print(self.arduino.set_negative_Z())
    
    #Help message for set_negative_Z.
    def help_set_negative_Z(self):
        print("This function sets the Z H-bridge to negative polarity. ")
        print("Accepted values are: 'Z'. ")
    
    #Deactivates all H-bridges. 
    def do_deactivate_all(self, _):
        if not self.mock:
            self.arduino.deactivate_all()
    
    #Help message for deactivate_all.
    def help_deactivate_all(self):
        print("This function deactivates all H-Bridges. ")
        print("Accepted values are: 'a'. ")
    
    #Deactivates the X H-bridge.    
    def do_deactivate_X(self, _):
        if not self.mock:
            self.arduino.deactivate_X()
    
    #Help message for deactivate_X.         
    def help_deactivate_X(self):
        print("This function deactivates just the X H-bridge. ")
        print("Accepted values are: 'b'. ")
    
    #Deactivates the Y H-bridge.    
    def do_deactivate_Y(self, _): 
        if not self.mock: 
            self.arduino.deactivate_Y()
    
    #Help message for deactivate_Y. 
    def help_deactivate_Y(self):
        print("This function deactivates just the Y H-bridge.")
        print("Accepted values are: 'c'. ")
    
    #Deactivates the Z H-bridge. 
    def do_deactivate_Z(self, _): 
        if not self.mock:
            self.arduino.deactivate_Z()
    
    #Help message for deactivate_Z.         
    def help_deactivate_Z(self): 
        print("This function deactivates just the Z H-bridge. ")
        print("Accepted values are: 'd'. ")
    
    #Returns the status of all 3 H-bridges.     
    def do_bridge_status(self, _):
        if not self.mock:
            print(self.arduino.get_bridge_status())
    
    #Help message for bridge_status. 
    def help_bridge_status(self):
        print("This function returns the status of all 3 H-bridges. ")
        print("1 = Bridge set to positive polarity. ")
        print("2 = Bridge set to negative polarity. ")
        print("0 = Bridge is turned off. ")
        print("Accepted values are: 's'. ")
    
    #Calibration function prototype
    def do_calibration(self, _):
        if not self.mock:
            Utilities.calibration(self.utility)
            self.psu['X'].set_output(0)
            self.psu['Y'].set_output(0)
            self.psu['Z'].set_output(0)
                
    #Calibration function help message.                 
    def help_calibration(self): 
        print("Testing help message for the calibration function. This is a WIP.")                

    def do_calibrate_axis(self, axis):
        # calibrate a single axis
        print(self.utility.calibrate_axis(axis.upper()))
    
    def help_calibrate_axis(self):
        print("Performs a linear regression on a single axis")
                
    #Retrieve the meter's current properties. 
    def do_meter_properties(self, _):
        if not self.mock:
            print(self.meter.meter_properties())
     
    #Meter properties help message. 
    def help_meter_properties(self):
        print("This function lists out the magnetometer's current properties. Should be listed.\n")
        print("The command for this function is 0x01. To run, just type 'meter_properties'. \n")
               
    #Retrieve user values that define the meter's behavior. 
    def do_meter_values(self, _):
        if not self.mock:
            self.meter.meter_value_settings()
    
    #Changable meter values help message. 
    def help_meter_values(self):
        print("This function returns the data values that can be changed by the user that define the meter's behavior. \n")
        print("This function's command is 0x02")
        
    #VAR_ADC_SETT tag function for meters that have it. 
    def do_var_tag(self, _):
        if not self.mock:
            self.meter.var_adc_settings()
            
    #VAR_ADC_SETT tag help function. 
    def help_var_tag(self):
        print("This function only works on meters with the VAR tag. Returns nothing if the meter doesn't have it. \n")
    
    #Stream data from the meter. (WIP)
    def do_stream(self, _):
        if not self.mock:
            print(self.meter.stream_data())
    
    #Stream data function help message. 
    def help_stream(self):
        print("This command returns the current magnetometer readings.")
        print("To run this command, run 'stream'. \n")
        print("READING FORMAT:\n")
        print("X-AXIS READING: \n")
        print("Y-AXIS READING: \n")
        print("Z-AXIS READING: \n")
        print("READING MAGNITUDE: \n")
        
    #Reading the averages of all 3 axes mag. field readings. 
    def do_average(self, _):
        if not self.mock:
            self.utility.reading_avg()
            
    #Prototype function. 
    def do_set_field(self, arg):
        (mG_x, mG_y, mG_z) = arg.split(" ")
        target = []
        for idx,mG in enumerate((mG_x, mG_y, mG_z)):
            try:
                target.append(int(mG))
            except: ValueError
        self.utility.set_field_vector(target)
            
    #Prototype help message.
    def help_set_field(self):
        print("This command sets and outputs a magnetic field vector.")
        print("Arguments are integers seperated by spaces")
        print("Eg. 10 20 30 attempts to form X:10 Y:20 Z:30")

    def do_receive_sim_data(self, _):
        if not self.mock:
            self.utility.receive_sim_data()

    def help_recieve_sim_data(self):
        print("This function listens for and unpacks data from the oresat simulator")
        print("To run this command, run 'recieve_sim_data'.\n")
        print("See documentation for further details.")

    def do_run_sim(self, _):
        if not self.mock:
            self.utility.run_sim()

    def help_run_sim(self):
        print("Produces the magnetic field data from most recent basilisk packet")
        print("Run 'run_sim' to start")

    #Closes program and exits. 
    def do_exit(self, _):
        print("Disabling power supplies.")
        self.psu['X'].set_output(0)
        self.psu['Y'].set_output(0)
        self.psu['Z'].set_output(0)
        return True
    
    #Help message for exit program.
    def help_exit(self):
        print("Type in exit to close the program ")
