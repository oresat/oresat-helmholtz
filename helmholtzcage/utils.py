#Utils.py library
#Author(s): Gustavo A. Cotom
#This file contains the utility functions needed to calibrate the PSAS Helmholtz Cage. 

import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from .Magnetometer import Magnetometer, MagnetometerCommands

class Utilities:
    #Class utilities constructor.
    def __init__(self, meter: Magnetometer):
        super().__init__()
        self.meter = meter
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
                print("sum_x:",sum_x)                
                sum_y += chunk[2]['value']
                print("sum_y:", sum_y)
                sum_z += chunk[3]['value']
                print("sum_z:", sum_z)
                #count += 1
            else:
                print("Warning: bad data encountered.")
        
        #Now find the averages of all 3 axes.
        x_avg = sum_x/num_iterations 
        y_avg = sum_y/num_iterations
        z_avg = sum_z/num_iterations


        print("x avg:", x_avg)
        print("y avg:", y_avg)
        print("z avg:", z_avg)           
        
        #Negated. 
        negated_x = 0 - x_avg 
        negated_y = 0 - y_avg
        negated_z = 0 - z_avg
        negate = []
        negate.append(x_avg, y_avg, z_avg)
        return negate
        
    
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
        
    def to_output_current(self, *raw_currents):
       # Maps theoretical current value to an output current to adjust for power supply errors
       slope = 1.23
       y_int = 28.3
       out_curr_vec = np.array(raw_currents)
       out_curr_vec = (out_curr_vec + 28.3) // 1.23
       return out_curr_vec

    def to_output_mag(self, raw_mag, ambient_mag):
       # Adjusts  magnetic field vector for output errors
       if len(raw_mag) < 3:
           print("Error: Magnetic field vector must have length 3, got {}".format(len(raw_mag)))
           return np.array([0, 0, 0])
       else:
           xyz_slope = np.array([-1.27, 1.27, -1.1])
           raw_mag = np.array(raw_mag)
           ambient_mag = np.array(ambient_mag)
           out_mag = (raw_mag - ambient_mag) // xyz_slope
           return out_mag

