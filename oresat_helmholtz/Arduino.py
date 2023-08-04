#This file enables communication with the Arduino which will control 3 H-Bridges (X,Y,Z) and initialized and interact with the magnetometer
#Documentation for Serial Commands: https://github.com/oresat/oresat-helmholtz/blob/main/Arduino_Comms/COMMS_README.txt
#Data Sheet

import serial
import serial.tools.list_ports
from enum import Enum

class ArduinoCommands(Enum):
	'''The following are the commands the arduino is listening for without any serial data returned'''
	POSITIVE_X = 'x'
	'''Activate X H-bridge in Positive Polarity'''
	POSITIVE_Y = 'y'
	'''Activate Y H-bridge in Positive Polarity'''
	POSITIVE_Z = 'z'
	'''Activate Z H-bridge in Positive Polarity'''
	NEGATIVE_X = 'X'
	'''Activate X H-bridge in Negative Polarity'''
	NEGATIVE_Y = 'Y'
	'''Activate Y H-bridge in Negative Polarity'''
	NEGATIVE_Z = 'Z'
	'''Activate Z H-bridge in Negative Polarity'''

	DEACTIVATE_ALL = 'a'
	'''De-activates all H-Bridges'''

	DEACTIVATE_X = 'b'
	'''De-Activate X H-Bridge'''
	DEACTIVATE_Y = 'c'
	'''De-Activate Y H-Bridge'''
	DEACTIVATE_Z = 'd'
	'''De-Activate Z H-Bridge'''

	'''The following are the commands the arduino is listening for with a serial data return'''
	MAGNETOMETER_READING = 'm'
	'''Request current magnetic field reading
	Data return is "X,Y,Z" magnetic field in uT. 
	The values of each value X,Y,Z can be positive or negative
	Here is an example return: "1000.05, -200.33, 500.79"
	Note: Refer to the nomen on the magnetometer to interpret positive and negative field directions'''

	MAGNETOMETER_STATUS = 'q'
	'''Data return is "0" -- magnetometer not initialized
		       	  "1" -- magnetometer is initialized
	note: magnetometer is initialized on setup/startup of arduino script.
	Restarting the serial interface will reset the arduino and will attempt re-initialization. 
	If failures persist inspect wiring to sensor and the physical sensor.'''

	H_BRIDGE_STATUS = 's'
	'''Query the H-Bridge's status:
	Data return is "XYZ" where
	X is X axis H-Bridge status
	Y is Y axis H-Bridge status
	Z is Z axis H-Bridge status
	Each position can be 0, 1, or 2: 
	0: Bridge is de-activated 
	1: Bridge is activated in positive polarity
	2: Bridge is activated in negative polarity
	Example:
	021
	X axis H-Bridge	is de-activated
	Y axis H-Bridge is activated in negative polarity
	Z axis H-Bridge is activated in positive polarity'''

	MAGNETOMETER_TEMP = 't'
	'''Request Ambient Temperature from Magnetometer: 
	The magnetometer has a temperature sensor built in, might as well provide the ability to read it. 
	The serial data return is in degrees Celcius:
	##.##
	Example: 17.80'''


class Arduino:

    #Serial communication settings for the Arduino Nano.	
    BAUDRATE = 115200
    INPUT_DELAY = 0.001
    BYTESIZE = serial.EIGHTBITS
    PARITY  = serial.PARITY_NONE
    STOPBITS = serial.STOPBITS_ONE
    TIMEOUT = 1

    def __init__(self, name: str):
        '''Object Construction. Passes the name of the arduino's USB port'''
        serial_port = None
        for i in serial.tools.list_ports.comports():
            if i.name == name:
                serial_port = i.device
                break
        if serial_port is None:
            raise Exception(f'Could not ind device with id of {name}')
	
        self.ser = serial.Serial(
            port = serial_port,
            baudrate = self.BAUDRATE,
            parity = self.PARITY,
            stopbits = self.STOPBITS,
            bytesize = self.BYTESIZE,
            timeout = self.TIMEOUT	
	)

    def write_message(self, msg):
        '''writes a command to serial port'''
        if self.ser.out_waiting != 0:
            self.ser.flush()
       
        self.ser.write(msg)
        self.ser.flush()

    def read_message(self, ending_token = '\n'):
        '''reads from serial port until a specific character'''
        data = self.ser.read_until(ending_token)
        return data.decode().strip()

    def send_command(self, msg):
        '''sends a command to serial port and reads the message returned'''
        self.write_message(msg)
        return self.read_message()

    def create_command(self, command):
        '''creates command to send through serial port'''
        '''<A> is address, ends on <\n>, and encode as bytes'''
        msg = f'A{command}\n'.encode()
        return msg

#definitions for function that help operate the commands. 	
    @property
    def set_positive_X(self) -> str:
        '''str: set X H-bridge to positive polarity'''
        msg = self.create_command(ArduinoCommands.POSITIVE_X.value)
        return self.send_command(msg)

    @property
    def set_positive_Y(self) -> str:
        '''str: set Y H-bridge to positive polarity'''
        msg = self.create_command(ArduinoCommands.POSITIVE_Y.value)
        return self.send_command(msg)

    @property
    def set_positive_Z(self) -> str:
        '''str: set Z H-bridge to positive polarity'''
        msg = self.create_command(ArduinoCommands.POSITIVE_Z.value)
        return self.send_command(msg)

    @property
    def set_negative_X(self) -> str:
        '''str: set X-bridge to negative polarity'''
        msg = self.create_command(ArduinoCommands.NEGATIVE_X.value)
        return self.send_command(msg)

    @property
    def set_negative_Y(self) -> str:
        '''str: set Y-bridge to negative polarity'''
        msg = self.create_command(ArduinoCommands.NEGATIVE_Y.value)
        return self.send_command(msg)

    @property
    def set_negative_Z(self) -> str:
        '''str: set Z-bridge to negative polarity'''
        msg = self.create_command(ArduinoCommands.NEGATIVE_Z.value)
        return self.send_command(msg)

    @property	
    def deactivate_all(self) -> str:
        '''str: deactivates all H-Bridges at the same time.'''
        msg = self.create_command(ArduinoCommands.DEACTIVATE_ALL.value)	
        return self.send_command(msg)

    @property
    def deactivate_X(self) -> str:
        '''str: turn off X H-bridge'''
        msg = self.create_command(ArduinoCommands.DEACTIVATE_X.value)
        return self.send_command(msg)

    @property	
    def deactivate_Y(self) -> str:
        '''str: turn off Y H-bridge'''
        msg = self.create_command(ArduinoCommands.DEACTIVATE_Y.value)
        return self.send_command(msg)
	
    @property
    def deactivate_Z(self) -> str:
        '''str: turn off Z H-bridge'''
        msg = self.create_command(ArduinoCommands.DEACTIVATE_Z.value)
        return self.send_command(msg)

    @property 
    def magnetometer_reading(self) -> str:
        '''str: return current magnetic field reading'''
        msg = self.create_command(ArduinoCommands.MAGNETOMETER_READING.value)
        return self.send_command(msg)	

    @property
    def magnetometer_status(self) -> str:
        '''str: returns 0 if magnetometer not initialized. 1 otherwise.'''
        msg = self.create_command(ArduinoCommands.MAGNETOMETER_STATUS.value)
        return self.send_command(msg)

    @property
    def bridge_status(self) -> str: 
        '''str: data return off current status of each H-bridge'''
        msg = self.create_command(ArduinoCommands.H_BRIDGE_STATUS.value)
        return self.send_command(msg)
	
    @property
    def magnetometer_temp(self) -> str:
        '''str: requests the ambient temperature of magnetometer.'''
        msg = self.create_command(ArduinoCommands.MAGNETOMETER_TEMP.value)
        return self.send_command(msg)








	






