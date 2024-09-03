#Utils.py library
#Author(s): Gustavo A. Cotom
#This file contains the utility functions needed to calibrate the PSAS Helmholtz Cage. 

import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from .Magnetometer import Magnetometer, MagnetometerCommands
from .Arduino import Arduino, ArduinoCommands
from .ZXY6005s import ZXY6005s, ZXY6005sCommands

class Utilities:
    #Class utilities constructor.
    def __init__(self, meter: Magnetometer, arduino: Arduino, psu: ZXY6005s):
        super().__init__()
        self.meter = meter
        self.arduino = arduino
        self.psu = psu
        pass
    
    ##Prototype function to calculate the milligauss averages of all 3 axis using the STREAM function. (WIP)
    def reading_avg(self): 
        #Variables needed. 
        sum_x = 0
        sum_y = 0
        sum_z = 0
        count = 0
        
        #Iterate and get 10 readings. 
        num_iterations = 10
        for _ in range(num_iterations):
            chunk = self.meter.stream_data() 
            if (chunk != []):
                sum_x += chunk[1]['value']
                # print("sum_x:",sum_x)                
                sum_y += chunk[2]['value']
                # print("sum_y:", sum_y)
                sum_z += chunk[3]['value']
                # print("sum_z:", sum_z)
                count += 1
            else:
                print("Warning: bad data encountered.")
        
        #Now find the averages of all 3 axes.
        x_avg = sum_x/count
        y_avg = sum_y/count
        z_avg = sum_z/count

        print("x avg:", x_avg)
        print("y avg:", y_avg)
        print("z avg:", z_avg) 
        
        mag_readings = np.array([x_avg, y_avg, z_avg])
        return mag_readings
        
    
    ''' Deprecating
    #Prototype function for getting the currents needed to match to earth's magnetic field. 
    def magnetic_to_current_zero(self):
        #This function to zero out the field in the cage utilizes the negated averages of each cage axis. 

        #First, get the y-value (y = desired_mag_field - mag_averages)
        data = self.reading_avg() #Call the reading average function and store the data.
        adjusted_field_x = 0 - data[0]
        adjusted_field_y = 0 - data[1]
        adjusted_field_z = 0 - data[2]
        
        print(f"Negated x_axis average:", adjusted_field_x)
        print(f"Negated y axis average:", adjusted_field_y)
        print(f"Negated z axis average:", adjusted_field_z)
        # currents = [-1000, -900, -800, -700, -600, -500, -400, -300, -200, -100, 0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

        ambient_mag = np.array([adjusted_feild_x, adjusted_field_y, adjusted_field_z])
        return ambient_mag
    '''
        
    def to_output_current(self, target_currents):
       # Maps theoretical current value to an output current to adjust for power supply errors
       if len(target_currents) < 3:
           print("Error: Target current provided to 'to_output_current()' must be size (3). Got ({})".format(len(target_currents)))
       slope = np.array([1.22, 1.23, 1.25])
       y_int = np.array([26.4, 33.6, 25])
       out_curr_vec = np.array(target_currents)
       out_curr_vec = (out_curr_vec - y_int) // slope
       return out_curr_vec

    def mag_to_current(self, target_mag, ambient_mag):
       # Adjusts magnetic field vector to remove ambient influences and system error
       if len(target_mag) < 3:
           print("Error: Magnetic field vector must have length 3, got {}".format(len(target_mag)))
           return np.array([0, 0, 0])
       else:
           xyz_slope = np.array([-1.27, 1.27, -1.1])    # hard-coded slope for linearly approximated output curve
           ambient_mag = np.array(ambient_mag)          # recorded ambient temperature
           target_mag = np.array(target_mag)
           out_mag = (target_mag - ambient_mag) // xyz_slope
           return out_mag
    
    def set_field_vector(self, target):
        # Attempts to set magnetic field in cage to the specified vector, assuming zero if argument is left empty
        out_field = np.array(target)          # xyz targets from arguments
        print("Setting magnetic field to target vector : {}, {}, {}".format(*out_field))

        # calculating current settings
        ambient_field = self.reading_avg()
        target_current = self.mag_to_current(out_field, ambient_field)
        out_current = self.to_output_current(target_current)
        
        if (out_current.min() < -800 or out_current.max() > 800):
            print("output currents are out of range!!\ncancelling output")
            return -1

        # updating H-Bridges
        self.arduino.set_positive_X() if out_current[0] > 0 else self.arduino.set_negative_X()
        self.arduino.set_positive_Y() if out_current[1] > 0 else self.arduino.set_negative_Y()
        self.arduino.set_positive_Z() if out_current[2] > 0 else self.arduino.set_negative_Z()

        # updating PSUs
        for i, dev in enumerate(['X', 'Y', 'Z']):
            self.psu.set_current_limit(dev, int(abs(out_current[i])))

        # powering up PSUs
        for dev in ['X', 'Y', 'Z']:
            self.psu.set_output(dev, int(1))

        return 0
