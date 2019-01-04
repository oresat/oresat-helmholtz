#function to set voltage. 1st parameter is voltage, 2nd is PSU #
def setVolts(voltage, psu):
        
        time.sleep(.1)
        if(psu == 1):
                ser1.write("Asu" + str(voltage * 100) + "\n")
        elif(psu == 2):
                ser2.write("Asu" + str(voltage * 100) + "\n")
        elif(psu == 3): 
                ser3.write("Asu" + str(voltage * 100) + "\n")

#function to set amps. 1st parameter is amps, 2nd is PSU #
def setAmps(amps, psu):
        
        time.sleep(.1)
        if(psu == 1):
                ser1.write("Asi" + str(amps * 1000) + "\n")
        elif(psu == 2):
                ser2.write("Asi" + str(amps * 1000) + "\n")
        elif(psu == 3): 
                ser3.write("Asi" + str(amps * 1000) + "\n")

#function to turn on/off PSU. 1st param: 1 = on, 0 = off, 2nd param: PSU #
def setOutput(onoff, psu):
        
        time.sleep(.1)
        if(psu == 1):
                ser1.write("Aso" + str(onoff) + "\n")
        elif(psu == 2):
                ser2.write("Aso" + str(onoff) + "\n")
        elif(psu == 3): 
                ser3.write("Aso" + str(onoff) + "\n")
        
def turnAllOff():
        
        time.sleep(.1)
        ser1.write("Aso0\n")
        time.sleep(.1)
        ser2.write("Aso0\n")
        time.sleep(.1)
        ser3.write("Aso0\n")
         
                
def turnAllOn():
        
        time.sleep(.1)
        ser1.write("Aso1\n")
        time.sleep(.1)
        ser2.write("Aso1\n")
        time.sleep(.1)
        ser3.write("Aso1\n")

import serial
import time

#Initialize serial ports
ser1 = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

print(ser1.name)  

ser2 = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

print(ser2.name)  

ser3 = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

print(ser3.name)  

control = 1

while (control != 0):
        #turnAllOff()

        print("\nPlease enter a command.")
        print("0 to Exit program \n1 to set Voltage \n2 to set Amperage")
        print("3 to turn On PSU's \n4 to turn Off PSU's\n")

        try:
                control = int(raw_input('Option selected: '))

                if control == 0:
                        print("\nExiting...")
                      
                elif control == 1:
                        v1 = float(raw_input('Enter desired Voltage: '))
                        p1 = int(raw_input('Select the power supply: '))

                        setVolts(v1, p1)
                        print("\nVoltage set to %s on PSU %d." % (v1, p1))

                elif control == 2:
                        a1 = float(raw_input('Enter desired Amperage: '))
                        p1 = int(raw_input('Select the power supply: '))

                        setAmps(a1, p1)
                        print("\nAmperage set to %s on PSU %d." % (a1, p1))

                elif control == 3:
                        turnAllOn()
                        print("Powering On...")

                elif control == 4:
                        turnAllOff()
                        print("Powering Off...")

                """#Set voltages
                
                setVolts(5, 1)
                setVolts(7, 2)
                setVolts(9, 3)
                
                #Set amps
                setAmps(.1, 1)
                setAmps(.3, 2)
                setAmps(.5, 3)

                time.sleep(3)

                turnAllOn()

                time.sleep(3)

                #turnAllOff()

                turnAllOff()

                #Set voltages
                
                setVolts(10, 1)
                setVolts(12, 2)
                setVolts(14, 3)
                
                #Set amps
                setAmps(.2, 1)
                setAmps(.4, 2)
                setAmps(.6, 3)
                """
                #time.sleep(3)

                #turnAllOn()
        except ValueError:
                print("\n***Invalid Entry***")

#time.sleep(3)


