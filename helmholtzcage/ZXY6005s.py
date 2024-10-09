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

    def __init__(self, location):
        '''construct objects, using location for X, Y and Z power supplies'''
        for i in serial.tools.list_ports.comports():
            if i.location == location:
                self.ser = serial.Serial(
                        port = i.device,
                        baudrate = self.BAUDRATE,
                        parity = self.PARITY,
                        stopbits = self.STOPBITS,
                        bytesize = self.BYTESIZE,
                        timeout = self.TIMEOUT,
                )
                break
            else:
                raise Exception(f'Could not find device {location}')


    def send_command(self, device_name, command):
        '''sends a command to serial port and reads the message returned'''
        self.ser.write(f'A{command}\n'.encode())
        self.ser.flush()
        return self.ser.readline().decode().strip()

    def model(self) -> str:
        ''' returns the model of power supply unit'''
        return self.send_command(ZXY6005sCommands.MODEL.value)

    def firmware_version(self, device_name: str) -> str:
        '''returns the firmware version'''
        return self.send_command(ZXY6005sCommands.FIRMWARE_VERSION.value)

    def set_output(self, power: bool):
        '''takes a boolean: 1 for ON, 0 for OFF to set output ON/OFF'''
        if power:
            command = f'{ZXY6005sCommands.SET_OUTPUT.value}1'
        else: 
            command = f'{ZXY6005sCommands.SET_OUTPUT.value}0'
        reply = self.send_command(command)
        if reply != command:
            raise ValueError(f'Invalid reply was {reply}, expected {command}')

    def set_amp_hour(self, mAh: int):
        '''takes an integer and sets amp hour counter to that value'''
        command = f'{ZXY6005sCommands.SET_AMP_HOUR.value}{mAh}'
        reply = self.send_command(command)
        if reply != command:
            raise ValueError(f'Invalid reply was {reply}, expected {command}')

    def return_amp_hour(self) -> int:
        '''returns amp hour reading'''
        return int(self.send_command(ZXY6005sCommands.RETURN_AMP_HOUR.value)[3:])

    def set_voltage(self, mV: int):
        '''takes an integer and sets voltage to that value in mV'''
        command = f'{ZXY6005sCommands.SET_VOLTAGE.value}{str(value)}'
        reply = self.send_command(command)
        if reply != command:
            raise ValueError(f'Invalid reply was {reply}, expected {command}')

    def return_voltage(self) -> int:
        '''takes a device name and returns voltage measurement'''
        return int(self.send_command(ZXY6005sCommands.RETURN_VOLTAGE.value)[3:])

    def set_current_limit(self, mA: int):
        '''takes an integer and sets current limit to that value in mA'''
        command = f'{ZXY6005sCommands.SET_CURRENT_LIMIT.value}{str(value)}'
        reply = self.send_command(command) 
        if reply != command:
            raise ValueError(f'Invalid reply was {reply}, expected {command}')

    def return_current(self) -> int:
        '''returns power supply current in amps'''
        return int(self.send_command(ZXY6005sCommands.RETURN_CURRENT.value)[3:])


    def return_mode(self) -> str:
        '''takes a device name and returns mode. see Data Sheet pg 6, Item 4'''
        reply = int(self.send_command(ZXY6005sCommands.RETURN_MODE.value)[3:])
        if reply == 1:
            return 'CC'
        else: 
            return 'CV'

    def return_temp(self) -> int:
        '''returns the power supply temperature in Celsius'''
        return int(self.send_command(ZXY6005sCommands.RETURN_TEMP.value)[3:])
