#Copy of ZXY6005s library. 
#Author: Teresa Labolle
#Documentation: INSERT STUFF HERE

import serial
import serial.tools.list_ports
from enum import Enum

class ZXY6005sCommands(Enum):
    MODEL = 'a'
    '''Get power supply unit model. Response: ZXY6005s.'''
    FIRMWARE_VERSION = 'v'
    '''Get firmware version. Response: R2.7Z'''
    SET_AMP_HOUR = 'sa'
    '''Set amp hour counter to specified value. Response: Asa(value)'''
    RETURN_AMP_HOUR = 'ra'
    '''Return the amp hour reading. Response: Ara(5 digit value)'''
    SET_VOLTAGE = 'su'
    '''Set voltage to specified value. Response: Asu(value)'''
    RETURN_VOLTAGE = 'ru'
    '''Return voltage measurement. Response: Aru(5 digit value)'''
    SET_CURRENT_LIMIT = 'si'
    '''Set current limit to specified value. Response: Asi(value)'''
    RETURN_CURRENT = 'ri'
    '''Return current in amps. Response: Ari(4 digit value)'''  
    RETURN_MODE = 'rc'
    '''Return current mode [Constant Voltage(CV) or Constant Current(CC)] Response: Arc0 or Arc1'''
    RETURN_TEMP = 'rt'
    '''Return temperature in Celsius. Response: Art(3 digit value)'''
    SET_OUTPUT = 'so'
    '''Set power output (On/Off). Response: Aso(1 or 0)'''

class ZXY6005s:
    BAUDRATE = 9600
    INPUT_DELAY = 0.001
    BYTESIZE = serial.EIGHTBITS
    PARITY = serial.PARITY_NONE
    STOPBITS = serial.STOPBITS_ONE
    TIMEOUT = 1

    def __init__(self):
        '''construct objects, using location for X, Y and Z power supplies'''
        names = ['X', 'Y', 'Z']
        locations = ['1-1.5.4.3', '1-1.5.4.2', '1-1.5.4.1']
        self.devices = {}
        for name, location in zip(names, locations):
            for i in serial.tools.list_ports.comports():
                if i.location == location:
                    self.devices[name] = serial.Serial(
                        port = i.device,
                        baudrate = self.BAUDRATE, 
                        parity = self.PARITY,
                        stopbits = self.STOPBITS,
                        bytesize = self.BYTESIZE, 
                        timeout = self.TIMEOUT,
                     )
                    break
        if len(self.devices) != 3:
            raise Exception(f'Could not find all 3 devices. ')

    def write_message(self, device_name, msg):
        '''writes a command to serial port'''
        ser = self.devices[device_name]
        if ser.out_waiting != 0:
            ser.flush()
        ser.write(msg)
        ser.flush()

    def read_message(self, device_name, ending_token = '\n'):
        '''reads from the serial port until a specified character'''
        ser = self.devices[device_name]
        data = ser.read_until(ending_token)
        return data.decode().strip()

    def send_command(self, device_name, msg):
        '''sends a command to serial port and reads the message returned'''
        self.write_message(device_name, msg)
        return self.read_message(device_name)

    def create_command(self, command):
        '''creates a command to send through the serial port'''
        '''<A> is address, end on <\n>, and encode as bytes'''
        msg = f'A{command}\n'.encode()
        return msg

    def model(self, device_name: str) -> str:
        '''takes a device name and returns the model name'''
        msg = self.create_command(ZXY6005sCommands.MODEL.value)
        return self.send_command(device_name, msg)

    def firmware_version(self, device_name: str) -> str:
        '''takes a device name and returns the firmware version'''
        msg = self.create_command(ZXY6005sCommands.FIRMWARE_VERSION.value)
        return self.send_command(device_name, msg)

    def set_output(self, device_name: str, value: bool):
        '''takes a device name and a boolean: 1 for ON, 0 for OFF to set output ON/OFF'''
        if value:
            msg = f'{ZXY6005sCommands.SET_OUTPUT.value}1'
        else: 
            msg = f'{ZXY6005sCommands.SET_OUTPUT.value}0'
        msg = self.create_command(msg)
        reply = self.send_command(device_name, msg)
        if reply != msg.decode().strip():
            raise ValueError(f'Invalid reply was {reply}, expected {msg.decode().strip()}')

    def set_amp_hour(self, device_name: str, value: int):
        '''takes a device name and an integer, sets amp hour counter to that value'''
        msg = f'{ZXY6005sCommands.SET_AMP_HOUR.value}{str(value)}'
        msg = self.create_command(msg)
        reply = self.send_command(device_name, msg)
        if reply != msg.decode().strip():
            raise ValueError(f'Invalid reply was {reply}, expected {msg.decode().strip()}')

    def return_amp_hour(self, device_name: str) -> int:
        '''takes a device name and returns amp hour reading'''
        msg = self.create_command(ZXY6005sCommands.RETURN_AMP_HOUR.value)
        raw = self.send_command(device_name, msg)
        return int(raw[3:])

    def set_voltage(self, device_name: str, value: int):
        '''takes a device name and an integer, sets voltage to that value'''
        msg = f'{ZXY6005sCommands.SET_VOLTAGE.value}{str(value)}'
        msg = self.create_command(msg)
        reply = self.send_command(device_name, msg)
        if reply != msg.decode().strip():
            raise ValueError(f'Invalid reply was {reply}, expected {msg.decode().strip()}')

    def return_voltage(self, device_name: str) -> int:
        '''takes a device name and returns voltage measurement'''
        msg = self.create_command(ZXY6005sCommands.RETURN_VOLTAGE.value)
        raw = self.send_command(device_name, msg)
        return int(raw[3:])

    def set_current_limit(self, device_name: str, value: int):
        '''takes a device name and an integer, sets current limit to that value'''
        msg = f'{ZXY6005sCommands.SET_CURRENT_LIMIT.value}{str(value)}'
        msg = self.create_command(msg)
        reply = self.send_command(device_name, msg) 
        if reply != msg.decode().strip():
            raise ValueError(f'Invalid reply was {reply}, expected {msg.decode().strip()}')

    def return_current(self, device_name: str) -> int:
        '''takes a device name and returns current in amps'''
        msg = self.create_command(ZXY6005sCommands.RETURN_CURRENT.value)
        raw = self.send_command(device_name, msg)
        return int(raw[3:])


    def return_mode(self, device_name: str) -> str:
        '''takes a device name and returns mode. see Data Sheet pg 6, Item 4'''
        msg = self.create_command(ZXY6005sCommands.RETURN_MODE.value)
        raw = self.send_command(device_name, msg)
        if int(raw[3:]) == 1:
            return 'CC'
        else: 
            return 'CV'

    def return_temp(self, device_name: str) -> int:
        '''takes a device name and returns temperature in Celsius (of PSU?)'''
        msg = self.create_command(ZXY6005sCommands.RETURN_TEMP.value)
        raw = self.send_command(device_name, msg)
        return int(raw[3:])
