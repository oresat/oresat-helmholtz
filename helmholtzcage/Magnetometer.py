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

    #Prototype read message function. Devs: please DO NOT delete any code until file is finalized!
    def proto_read_chunk(self):
        data = self.ser.read(20) #Read in 20 bytes.
        return data
    
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
    
    #Prototype function to handle meter's response. (Used for commands that deal with chunks)
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
        
        #Parse any data that was returned by the meter. 
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
            
    #Prototype function to handle the streaming of data. 
    def read_stream_data(self):
        #Read the initial chunk of data.
        stream_data = self.ser.read_until(b'\x08') #Read until the acknowledgment byte.
        
        #Remove the final acknowledgement byte from the stream data. 
        if stream_data[-1] == 0x08:
            stream_data = stream_data[:-1]
            
        #Determine the number of data points.
        num_data_points = len(stream_data) // 6
        
        point_dict = {
            0:"time",
            1:"x",
            2:"y",
            3:"z",
            4:"magnitude"
        }
        chunk = []

        #Process each data point.
        for i in range(num_data_points):
            data_point = stream_data[i*6:(i+1)*6]
            data = self.parse_data_point(data_point,point_dict[i])
            if data['config'] == 0:
                print("parsing failed - bad data")
                break
            chunk.append(data)
        print("Stream data processed successfully.")
        return chunk
        
    #Prototype function to parse through each data point received. 
    def parse_data_point(self, data_point, dict):
        #Convering the 6-byte data point into individual components.
        #Assuming data_point is a bytearray or bytes object.
        '''# new alternative below
        config_info = (data_point[0] << 4) | (data_point[1] >> 4) #12 bits for configuration. 
        sign_decimal_info = ((data_point[1] & 0x0F) << 4) | (data_point[2] >> 4) #4 bits for sign and decimal
        actual_number = struct.unpack(">I", data_point[2:6])[0] & 0xFFFFFFFF #32 bits for the actual number.
        
        print(f"Config Info: {config_info}, Sign/Decimal Info: {sign_decimal_info}, Number: {actual_number}")
        '''

        print("byte array", data_point)
        # FIXME : Test this code, then remove this comment when working
        config_info = data_point[0]                             # config info we don't use yet
        sign_decimal_info = data_point[1]                       # second byte tells sign and decimal place
        sign = -1 if (sign_decimal_info & 0x08) else 1          # if 4th msb is positive, the value is negative
        decimal_power = (sign_decimal_info & ~0xF8)             # 3 lsb denote power of 10 at decimal place

        raw_value = struct.unpack(">I", data_point[2:6])[0] & 0xFFFFFFFF # 32 bits for unsigned integer value of the data point
        value = (sign * raw_value) / (10.0 ** decimal_power)    # converts to signed float32
        print("Config info: {:b} Sign/Decimal: {:b} uInt Value: {} Value {}: {}".format(config_info, sign_decimal_info, raw_value, dict, value))
        return {'config' : config_info, 'sign' : sign, 'power' : decimal_power, 'raw_value' : raw_value, 'value' : value} 
        
                
    #ID_METER_PROP (0x01). Returns the current meter's properties.  
    def meter_properties(self):
        self.send_command(MagnetometerCommands.ID_METER_PROP.value)
        self.handle_meter_response()
    
    #ID_METER_SETT (0x02). Returns all user values that define desired behavior of the meter. 
    def meter_value_settings(self):
        self.send_command(MagnetometerCommands.ID_METER_SETT.value)
        self.handle_meter_response()
        
    #ID_METER_ADC_SETT (0x1C). Returns a list of meter ADC setting that are pre-defined, user selectable, 
    # configuration settings for the meter ADC(s).
    def var_adc_settings(self):
        self.send_command(MagnetometerCommands.ID_METER_ADC_SETT.value)
        self.handle_meter_response()
        
    #STREAM_DATA (0x03). Stream data function. (WIP)
    def stream_data(self):
        self.send_command(MagnetometerCommands.STREAM_DATA.value)
        self.read_stream_data()
        
    #Prototype function to calculate the milligauss averages of all 3 axis using the STREAM function. (WIP)
    def reading_avg(self):
        
        #Variables needed. 
        sum_x = 0
        sum_y = 0
        sum_z = 0
        count = 0
        
        #Iterate and get 10 readings. 
        num_iterations = 10
        for _ in range(num_iterations):
            chunk = self.stream_data() 
            if (chunk):
                sum_x += chunk[1]['value']
                sum_y += chunk[2]['value']
                sum_z += chunk[3]['value']
                count += 1
            else:
                print("Warning: bad data encountered.")
        
        #Now find the averages of all 3 axes.
        if (count) :
            x_avg = sum_x/count 
            y_avg = sum_y/count
            z_avg = sum_z/count
        else:
            print("boo boo ;(")

        print(x_avg)
        print(y_avg)
        print(z_avg)            
