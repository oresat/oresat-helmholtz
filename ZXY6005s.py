import serial
import time
#import utilities as utils #debugging
import struct

#v1.1_0514
# Library that manages the ZXY6005s power supply


#these functions to be used for later 
#raw bytes to a string
def as_string(raw_data):
	return bytearray(raw_data[:-1])

#raw bytes to a float
def as_float(raw_data):
	f = struct.unpack_from(">f", bytearray(raw_data))[0]
	return f

#raw bytes to a word
def as_word(raw_data):
	w = struct.unpack_from(">H", bytearray(raw_data))[0]
	return w


class ZXY6005s:
	def __init__(self, port,input_delay=utils.INPUT_DELAY,  baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1):
		self.port = port
		self.input_delay = input_delay
		self.baudrate = baudrate
		self.baudrate = baudrate
		self.parity = parity
		self.bytesize = bytesize
		self.timeout = timeout
		self.serial = None
 		utils.log(0, "Powersupply info:\n\tPort: " + str(port) + '\n\tInput delay: ' str(input_delay) + '\n\tBaud rate: ' + str(baudrate) + '\n\tParity: ' + str(parity) + '\n\t stop bits: ' + str(stopbits) + '\n\tByte Size: ' + str(bytesize) + '\n\tTimeout: ' + str(timeout))

	def is_open(self):
		return self.serial.is_open
	
	def get_device_information(self):
		return self.__device_information

	def disconnect(self):
		self.serial.close()

	def send_command(self, command):
		self.serial.write(command.encode())

	def set_voltage(self, voltage):
		self.send_command(f"VSET:{voltage:.2f}")

	def set_current(self, current):
		self.send_command(f"ISET:{current:.3f}")
	
	def enable_output(self):
		self.send_command("OUT1")

	def disable_output(self):
		self.send_command("OUT0")

	





	
#Notes
#Baudrate: speed of communication over a data channel
#Parity: bit added to a string as a form of error detection



