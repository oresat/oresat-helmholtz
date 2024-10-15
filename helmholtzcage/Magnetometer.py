#Author(s): Gustavo A. Cotom 
#Purpose: New Magnetometer Library (V1). 
#This file enables serial communication between the Helmholtz Cage and the new 
#Alphalab magnetometer. 

#Notes: This file follows a similar structure to the ZXY6005s and Arduino python libraries. 

import serial
import struct
import serial.tools.list_ports
from enum import Enum

#Magnetometer Commands Library.
class MagnetometerCommands(Enum):
    '''The following are the commands the sensor responds to through serial.'''
    ID_METER_PROP = 0x01 #See page 4 on the alphalab serial handbook for more information. 
    ID_METER_SETT = 0x02 #See page 6 on the alphalab serial handbook for more information.
    ID_METER_ADC_SETT = 0x1C #See page 7 on the alphalab serial handbook for more information.
    STREAM_DATA = 0x03 #See page 8 on the alphalab serial handbook for more information. 
    BREAK_SUSPEND = 0x14 # See page 20 of alphalab comm protocol
    KILL_PROC = 0xFF # Kills all processes and clears meter buffer
    ACK = 0x08
    
    #Add more commands here as we see fit. 

class Magnetometer:
    
    #Serial communication settings for the Arduino Nano.	
    BAUDRATE = 115200
    INPUT_DELAY = 0.001
    BYTESIZE = serial.EIGHTBITS
    PARITY  = serial.PARITY_NONE
    STOPBITS = serial.STOPBITS_ONE
    TIMEOUT = 1

    #Magnetometer class constructor. Serial setup done here.
    def __init__(self, location: str, serial_port=None):
        '''Object Construction. Passes the name of the Magnetometer's USB port'''
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
    
    def send_command(self, command=0x08):
        # sends a command, default is ACK
        command = [command]*6
        self.ser.write(bytearray(command))
        print(f"Sent: {command}")
      
    #Prototype function to handle meter's response. (Used for commands that deal with chunks)
    def read_ascii_stream(self):
        # parses data returned from magnetometer using ascii encoding, used for meter properties and settings
        ascii_response = ""
        chunk = None
        read_chunk = True
        timeouts = 0
        
        while read_chunk:
            chunk = self.ser.read_until(expected=b'\x08', size=20) # magnetometer sends data in 20-byte chunks
            
            if chunk:
                #Decoding the ASCII data.
                ascii_response += chunk.decode('ascii', errors='ignore').strip()
                
                #checking for the termination byte (0x07)
                if chunk[-1] == 0x07:
                    print("Termination byte received, ending communication.")
                    break
                else:
                    self.send_command(MagnetometerCommands.ACK.value)
            else:
                timeouts += 1
                print("No response recieved and communication timed out. Trying again")
                if timeouts > 5:
                    read_chunk = False
                    print("No data encountered in 20 chunks. Ending transmission.")
            
        #Parse any data that was returned by the meter. 
        response = {}
        properties = ascii_response.split(':')
        for prop in properties:
            if '=' in prop:
                key, value = prop.split('=', 1)
                response[key] = value
        return response

            
    def get_value(self, byte_array):
        # Decodes data point and returns integer value, data_point
        sign = -1 if (byte_array[1] & 0x08) else 1          # if 4th msb in byte2 is positive, the value is negative
        decimal_power = (byte_array[1] & ~0xF8)             # 3 lsb denote power of 10 at decimal place

        raw_value = struct.unpack(">I", byte_array[2:6])[0] & 0xFFFFFFFF # 32 bits for unsigned integer value of the data point
        value = (sign * raw_value) / (10.0 ** decimal_power)    # converts to signed float32
        return value

    def stream_data(self):
        # requests and recieves data points from magnetometer
        no_ack = 1
        timeouts = 0
        data = []

        self.send_command(MagnetometerCommands.STREAM_DATA.value) # request data
        while no_ack:
            point = self.ser.read_until(b'\x08', size=6)  # read until the acknowledgment byte
            if point:
                if point == b'\x08':
                    no_ack = 0 # got ACK byte, ending transmission
                else:
                    data.append(self.get_value(point))
            else:
                timeouts += 1
                print("Data stream timed out, trying again.")
                if timeouts > 4:
                    print("No data encountered. Returning zeros.")
                    data = [0, 0, 0, 0, 0]
                    break

        self.send_command(MagnetometerCommands.KILL_PROC.value) # clears buffer
        return data
            
    def get_full_datapoint(self, byte_array):
        #Convering the 6-byte data point into individual components.
        #Assuming data_point is a bytearray or bytes object.
        config_info = byte_array[0]                             # config info we don't use yet
        sign = -1 if (byte_array[1] & 0x08) else 1          # if 4th msb is positive, the value is negative
        decimal_power = (byte_array[1] & ~0xF8)             # 3 lsb denote power of 10 at decimal place

        raw_value = struct.unpack(">I", byte_array[2:6])[0] & 0xFFFFFFFF # 32 bits for unsigned integer value of the data point
        value = (sign * raw_value) / (10.0 ** decimal_power)    # converts to signed float32
        return {'config' : config_info, 'sign' : sign, 'power' : decimal_power, 'raw_value' : raw_value, 'value' : value} 
        
                
    #ID_METER_PROP (0x01). Returns the current meter's properties.  
    def meter_properties(self):
        self.send_command(MagnetometerCommands.ID_METER_PROP.value)
        return self.read_ascii_stream()
    
    #ID_METER_SETT (0x02). Returns all user values that define desired behavior of the meter. 
    def meter_value_settings(self):
        self.send_command(MagnetometerCommands.ID_METER_SETT.value)
        return self.read_ascii_stream()
        
    #ID_METER_ADC_SETT (0x1C). Returns a list of meter ADC setting that are pre-defined, user selectable, 
    # configuration settings for the meter ADC(s).
    def var_adc_settings(self):
        self.send_command(MagnetometerCommands.ID_METER_ADC_SETT.value)
        return self.read_ascii_stream()
        
