#Utils.py library
#Author(s): Gustavo A. Cotom
#This file contains the utility functions needed to calibrate the PSAS Helmholtz Cage. 

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
        
        print(f"Negated x_axis average:", negated_x)
        print(f"Negated y axis average:", negated_y)
        print(f"Negated z axis average:", negated_z)