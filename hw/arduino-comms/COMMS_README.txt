COMMS_README.TXT

This document is the decode key to "ArduinoComms.py" and "PSAS_HHCage.ino"

General:
The arduino will initialize the magnetic sensor (if present) and listen on USB-Serial (115200) for one byte messages from the Raspberry PI / Python. The Arduino will control 3 H-bridges (X,Y,Z) and interact with a magnetometer (MMC5603). Some commands from the PI will recieve a serial data return.

Note that decode values are case sensitive.The following are the commands the arduino is listening for without any serial data returned: 
x - Activate X H-bridge in Positive Polarity
y - Activate Y H-bridge in Positive Polarity
z - Activate Z H-bridge in Positive Polarity
X - Activate X H-bridge in Negative Polarity
Y - Activate Y H-bridge in Negative Polarity
Z - Activate Z H-bridge in Negative Polarity
a - De-activate all H-Bridges (X,Y,Z)
b - De-activate X H-Bridge
c - De-activate Y H-Bridge
d - De-activate Z H-Bridge
The following are the commands the arduino is listening for with a serial data return:
m - Request current magnetic field reading
	Data return is "X,Y,Z" magnetic field in uT.
	The values of each value X,Y,Z can be positive or negative
	Here is an example return: "1000.05,-200.33,500.79"
	Note: Refer to the nomen on the magnetometer to interpret positive and negative field directions
q - Request magnetometer status
	Data return is "0" -- magnetometer not initialized
		       "1" -- magnetometer is initialized
	note: magnetometer is initialized on setup/startup of arduino script. Restarting the serial interface will reset the arduino and will attempt re-initialization. If failures persist inspect wiring to sensor and the physical sensor.
s - Request H-Bridge Status:
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
	X axis H-Bridge is de-activated
	Y axis H-Bridge is activated in negative polarity
	Z axis H-Bridge is activated in positive polarity
t - Request Ambient Temperature from Magnetometer:
	The magnetometer has a temperature sensor built in, might as well provide the ability to read it.
	The Serial data return is in degrees Celsius:
	##.##
	Example: 17.80

# Credit to Christian Bennett (2022) for assisting with Arduino code and testing