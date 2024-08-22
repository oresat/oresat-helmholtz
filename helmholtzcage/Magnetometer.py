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

    #def read_message(self, ending_token = '\n'):
        #'''reads from serial port until a specific character'''
        #data = self.ser.read_until(ending_token)
        #return data.decode().strip() 
    
    #Prototype read message function. Devs: please DO NOT delete any code until file is finalized!
    def proto_read_chunk(self):
        data = self.ser.read(20) #Read in 20 bytes.
        return data

    #def send_command(self, msg):
        #'''sends a command to serial port and reads the message returned'''
        #self.write_message(msg)
        #return self.read_message()
    
    #Prototype send message function. 
    def send_command(self, command, extra_bytes = None):
        command = [command] + (extra_bytes if extra_bytes else [0x00]* 5)
        self.ser.write(bytearray(command))
        print(f"Sent: {command}")
        
    #Prototype acknowledgment function. 
    def acknowledgment(self):
        ack_command = [0x08, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.ser.write(bytearray(ack_command))
        print("Sent acknowledgement")
    
        
    def create_command(self, command):
        '''creates command to send through serial port'''
        '''<A> is address, ends on <\n>, and encode as bytes'''
        msg = f'A{command}\n'.encode()
        return msg

    #Prototype function to handle meter's response.
    def handle_meter_response(self):
        full_response = ""
        
        while True:
            chunk = self.proto_read_chunk()
            
            if not chunk:
                print("No response or communication timeout.")
                break
            
            #Decoding the ASCII data.
            ascii_data = chunk.decode('ascii', errors='ignore').strip()
            full_response += ascii_data
            
            #checking for the termination byte (0x07)
            if chunk[-1] == 0x07:
                print("Termination byte received, ending communication.")
                break
            else:
                self.acknowledgment()
        
        self.parse_meter_response(full_response)
     
    #Parsing the data received from the meter.    
    def parse_meter_response(self, response):
        properties = response.split(':')
        parsed_data = {}
        
        for prop in properties:
            if '=' in prop:
                key, value = prop.split('=', 1)
                parsed_data[key] = value
                
        #Display the parsed properties.
        for key, value in parsed_data.items():
            print(f"{key}: {value}")
        

    #WIP of the first command. To all developers: comment out code you do not wish to use. 
    #def meter_properties(self) -> str: 
        #'''str: send the 0x01 command to retrieve the meter's current properties. '''
        #msg = self.create_command(MagnetometerCommands.ID_METER_PROP.value) #Creating the command 
        #return self.send_command(msg)
        
        
    #The meter will be returning a "confirmation byte" back along with the data needed. This logic will be placed in the
    #helmholtz shell file. 
