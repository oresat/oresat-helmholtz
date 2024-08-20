#Author(s): Gustavo A. Cotom 
#Purpose: New Magnetometer Library (V1). 
#This file enables serial communication between the Helmholtz Cage and the new 
#Alphalab magnetometer. 

#Notes: This file follows a similar structure to the ZXY6005s and Arduino python libraries. 

import serial
import serial.tools.list_ports
from enum import Enum

#Magnetometer Commands Library.
class MagnetometerCommands(Enum):
    '''The following are the commands the sensor responds to through serial.'''
    ID_METER_PROP = '0x01' #See page 4 on the alphalab serial handbook for more information. 
    
    #Add more commands here as we see fit. 

class Magnetometer:
    
    #Serial communication settings for the Arduino Nano.	
    BAUDRATE = 115200
    INPUT_DELAY = 0.001
    BYTESIZE = serial.EIGHTBITS
    PARITY  = serial.PARITY_NONE
    STOPBITS = serial.STOPBITS_ONE
    TIMEOUT = 1

    def __init__(self, location: str):
        '''Object Construction. Passes the name of the Magnetometer's USB port'''
        serial_port = None
        
        for i in serial.tools.list_ports.comports():
            if i.location == location:
                serial_port = i.device
                break
        if serial_port is None:
            raise Exception(f'Could not find device with location of {location}')
	
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

    #WIP of the first command. To all developers: comment out code you do not wish to use. 
    def meter_properties(self) -> str: 
        '''str: send the 0x01 command to retrieve the meter's current properties. '''
        msg = self.create_command(MagnetometerCommands.ID_METER_PROP.value) #Creating the command 
        self.send_command(msg)
        
        
    #The meter will be returning a "confirmation byte" back along with the data needed. This logic will be placed in the
    #helmholtz shell file. 
