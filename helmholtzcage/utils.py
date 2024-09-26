#Utils.py library
#Author(s): Gustavo A. Cotom, Emily Snodgrass, Daniel Monahan
#This file contains the utility functions needed to calibrate the PSAS Helmholtz Cage. 

import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import struct
import serial
import pprint
import time
from .Magnetometer import Magnetometer, MagnetometerCommands
from .ZXY6005s import ZXY6005s, ZXY6005sCommands
from .Arduino import Arduino, ArduinoCommands

MAX_OUT_CURRENT = 800                    # 1 amp limit
MAG_CURRENT_SLOPE = [-1.24, 1.25, -1.12] # Conversion factors for magnetic field to current relation
AMBIENT_FIELD = [226, 238, 401]         # (mG) Ambient field components recorded on 09/22/24

class Utilities:
    #Class utilities constructor.
    def __init__(self, meter: Magnetometer, psu:ZXY6005s, arduino:Arduino):
        super().__init__()
        self.meter = meter
        self.psu = psu
        self.arduino = arduino
        self.xyz_slope = MAG_CURRENT_SLOPE      # default calibration settings
        self.ambient_field = AMBIENT_FIELD      # default calibration settings
        self.bask_data = [[0, 0, 0]]            # register for basilisk data
    
    def convert_amp_val(self, val):
        #accounts for inconsistencies in the power converters by adjusting an amperage using a conversion factor
        final_val =  int((val-28.3)/1.23)
        if final_val < 0:
            final_val = 0
        return final_val

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
                count = count + 1
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
        self.ambient_field = mag_readings
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

        ambient_mag = np.array([adjusted_field_x, adjusted_field_y, adjusted_field_z])
        return ambient_mag
    '''
        
    def to_output_current(self, target_currents):
       # Maps theoretical current value to an output current to adjust for power supply errors
       if len(target_currents) < 3:
           print("Error: Target current provided to 'to_output_current()' must be size (3). Got ({})".format(len(target_currents)))
           return np.array([0, 0, 0])
       slope = np.array([1.22, 1.23, 1.25])
       y_int = np.array([26.4, 33.6, 25])
       out_curr_vec = np.array(target_currents)
       out_curr_vec = (out_curr_vec - y_int) // slope
       return out_curr_vec

    def mag_to_current(self, target_mag):
       # Adjusts magnetic field vector to remove ambient influences and system error using linear regression coefficients
       if len(target_mag) < 3:
           print("Error: Target field vector must have length 3, got {}".format(len(target_mag)))
           return np.array([0, 0, 0])
       else:
           target_mag = np.array(target_mag)
           xyz_slope = np.array(self.xyz_slope)                # slope of mag-current line
           ambient_mag = np.array(self.ambient_field)          # intercept of mag-current line

           out_mag = (target_mag - ambient_mag) // self.xyz_slope
           return out_mag
    
    def set_field_vector(self, target=[0, 0, 0]):
        # Attempts to set magnetic field in cage to the specified vector, assuming zero if argument is left empty
        out_field = np.array(target)            # xyz targets from arguments
        ambient_field = np.array(self.ambient_field) # average field from earth
        xyz_slope = np.array(self.xyz_slope)

        if (out_field.shape != (3,) or ambient_field.shape != (3,)):
            print("Error: Vectors provided to set_field_vector() must be of shape (3,). Got {} and {}.".format(out_field.shape, ambient_field.shape) )
            return -1

        # calculating current settings
        out_current = self.mag_to_current(out_field)
        
        if (np.abs(out_current).max() > MAX_OUT_CURRENT):
            print("output currents are out of range!!\ncancelling output")
            return -1

        print("Setting magnetic field to target vector :", out_field)#{}, {}, {}".format(*out_field))

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
    
       
    def calibration(self):
        #Current values.
        max_current = 1000
        min_current = 0 
        step = 100
        
        #Opening and declaring headers for the CSV file.
        # with open("cage_cal.csv", "w") as new_file:
        #     fieldnames = ['Current (A)', 'Magnetic Field X (T)', 'Magnetic Field Y (T)', 'Magnetic Field Z (T)']
        #     csv_writer= csv.DictWriter(new_file, fieldnames = fieldnames, delimiter='\t')
        #     csv_writer.writeheader()
        
        
        ''' Deprecating
        for i in 'XYZ':
            #Making sure all power supplies are off by default.
            self.psu.set_output('X', 0)
            self.psu.set_output('Y', 0)
            self.psu.set_output('Z', 0)
            
            self.psu.set_output(i, 1)

            #Setting X, Y and Z bridges to negative polarity.
            if i == 'X': 
                self.arduino.set_negative_X()
            
            elif i == 'Y': 
                self.arduino.set_negative_Y()
                
            elif i == 'Z': 
                self.arduino.set_negative_Z()
            
            #Iterating starting at -1 amps to 0 amps. 
            for current_val in range(max_current, min_current, -step):
                current_val = self.convert_amp_val(current_val)
                self.psu.set_current_limit(i, current_val)
                current_val = self.psu.return_current(i)
                print("current val -", current_val)

            #Setting X, Y and Z bridges to positive polarity.
            if i == 'X': 
                self.arduino.set_positive_X()
            
            elif i == 'Y': 
                self.arduino.set_positive_Y()
                
            elif i == 'Z': 
                self.arduino.set_positive_Z()
            
            #Iterating starting at 0 amps to 1 amps. 
            for current_val in range(min_current, max_current + step, step):
                current_val = self.convert_amp_val(current_val)
                self.psu.set_current_limit(i, current_val)
                current_val = self.psu.return_current(i)
                print("current val +", current_val)
        '''
        #Prototype calibration v2. Running calibration on all 3 PSUs at once instead of continously. 
        #Initial check: making sure all PSUs are off. 
        self.psu.set_output('X', 0)
        self.psu.set_output('Y', 0)
        self.psu.set_output('Z', 0)
        
        #Powering up all PSUs
        self.psu.set_output('X', 1)
        self.psu.set_output('Y', 1)
        self.psu.set_output('Z', 1)
        
        #Setting all H-bridges to negative polarity.
        self.arduino.set_negative_X()
        self.arduino.set_negative_Y()
        self.arduino.set_negative_Z()
        
        #Iterating starting at -1000 mA to 0. 
        mags_rec = {'X': [], 'Y': [], 'Z': []}
        for idx, axis in enumerate(['X', 'Y', 'Z']):
            self.psu.set_current_limit('X', 0)
            self.psu.set_current_limit('Y', 0)
            self.psu.set_current_limit('Z', 0)
            for current_val in range(max_current, min_current, -step):
                current_val = self.convert_amp_val(current_val)
                self.psu.set_current_limit(axis, current_val)
                magdict = self.meter.stream_data()
                if magdict:
                    mag_val = magdict[idx]['value'] * magdict[idx]['sign']
                else:
                    mag_val = 0
                mags_rec[axis].append(mag_val)
                print(mags_rec)
            
        #Setting all H-bridges to positive polarity.
        self.arduino.set_positive_X()
        self.arduino.set_positive_Y()
        self.arduino.set_positive_Z()
        
        #Iterating starting at 0 mA to 1000.
        for idx, axis in enumerate(['X', 'Y', 'Z']):
            self.psu.set_current_limit('X', 0)
            self.psu.set_current_limit('Y', 0)
            self.psu.set_current_limit('Z', 0)
            for current_val in range(min_current, max_current, step):
                current_val = self.convert_amp_val(current_val)
                self.psu.set_current_limit(axis, current_val)
                magdict = self.meter.stream_data()
                if magdict:
                    mag_val = magdict[idx]['value'] * magdict[idx]['sign']
                else:
                    mag_val = 0
                mags_rec[axis].append(mag_val)
                print(idx, axis)

        print("Recorded calibration data...\n{}".format(mags_rec))

    def receive_sim_data(self):
        with serial.Serial(port="/dev/ttyUSB5", baudrate=115200) as ser:
            start = time.Time()
            success = False
            while (start - time.time() < 2) :
                # Continuously listen for serial data until it is recieved
                data = ser.read(1140)

                if len(data) > 0:
                    # Unpack the bytearrays containing data into vectors
                    new_array = [[x, y, z] for x, y, z in struct.iter_unpack('3f', data)]
                    success = True
                    pprint.pp(new_array) # FIXME: This line prints result for testing purposes
            if not success:
                print("Error: Receive sim data timed out!")
            else:
                self.bask_data = new_array

    def run_sim(self):
        # attempts to do the thing.
        for mag_vector in self.bask_data:
            self.set_field_vector(mag_vector)

    def linear_regression(x, y):
        # Performs 2-dim linear regression and returns a tuple of linear coefficients.
        num_points = np.size(x)
        
        # mean of x and y vectors
        mean_x = np.mean(x)
        mean_y = np.mean(y)
        
        # sum of cross and square deviations in xy and xx respectively
        sum_cross_xy = np.sum(y*x) - num_points*mean_x*mean_y
        sum_square_xx = np.sum(x*x) - num_points*mean_x*mean_x
        
        # calculating slope and intercepts
        m = sum_cross_xy / sum_square_xx
        y_0 = mean_y - m*mean_x
        return (m, y_0)
        
