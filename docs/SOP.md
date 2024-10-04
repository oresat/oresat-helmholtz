![alt text](https://user-images.githubusercontent.com/33878769/50576984-cde2d900-0dd2-11e9-8117-1c2e21f85c7d.png)

# OreSat Helmholtz Cage: Standard Operating Procedure

This Standard Operating Procedure contains information about safely operating the cage to avoid
potential injuries to the operator, and to avoid damaging the Helmholtz cage components. This is 
the place to start if you're hoping to run some simulations, test the cage operation, or simply
learn about how the cage is operated.


## General Notes:

### Maximum Operating Range!
In order to maintain operation of coil components, the Helmholtz cage operator must ensure
that commands they issue to the cage do not exceed these limits.
* Maximum Voltage across a single coil must not exceed 10V
* Maximum current through a single coil must not exceed 1 Amp at 10V for a 10W maximum.
* Hardware components must not exceed their maximum operating temperatures. See Safety for details.


### Analytical Field Control Model
* Theoretical magnetic field vector equation:
![alt text](https://user-images.githubusercontent.com/33878769/50580148-2381aa80-0e00-11e9-8fdd-0a406a66f1ba.png)
  * Bz is the total field produced by both square coils as a function of the axial distance z from the center of the coils
  * u0 is the permeability of free space: 4pi*10^-7 WB A^-1 m^-1
  * n is the number of turns of wire: 58 turns
  * I is the current of the wire being analyzed: user input
  * h is the distance between the coils: 
  * a is one half the side length of the structure: 

---
## Safety:

* The red coils will get hot if operated for an extended period of time at high currents. Do not touch or hold the coils when operating the cage.
* Monitor the temperature of the H-Bridges and wires to maintain a safe operating temperature below 140°C.
* Monitor the temperature of the main power supply to operate between -25°C to 70°C.
* If the temperature begins to approach the operating limits, turn off the power supply and let the cage cool down before resuming testing.

---
## Prepping the Cage:

1. It is *generally* safe to put electronic devices inside and around the cage. However, they may disrupt the magnetic field or magnetometer readings and cause discrepancies in testing data. Be mindful of this and be aware of the testing space surroundings.
2. Verify that the coils are secured in the terminal blocks and make sure they are connected to the correct terminals/power supply, see labels. No exposed or crossing wires!
3. Turn on the surge protector. This will power the raspberry pi, monitor, power supplies, magnetometer, and Arduino.
4. Turn on the Magnetometer by rotating the power knob to the 'On' position.
5. Let the Raspberry Pi boot up and power on the keyboard to operate the command line.

---
## Operating the Cage Program:

The Helmholtz command line program boots into a manual control mode in which you have complete 
control of the power supply, H-Bridges, and Magnetometer data. It is your responsibility as an 
operator to comply with the safety protocols and ensure that the maximum operating range is 
NOT EXCEEDED. Broken components are a total bummer and you don't want to have to be that guy. 
Refer to the General Notes and Safety sections of the SOP to get familiar. 

### Starting the Program
Now if you've just booted up the Rasberry Pi you'll have to launch the command line utility
using the python compiler. Here is how you do that:
1. Enter the oresat-helmholtz directory where the program is stored
```
$ cd ~/oresat-helmholtz
```
2. Run the python script which initializes the cage control modules. This requires that we provide
the USB bus locations of the Arduino nano and the Magnetometer. If nothing has been tampered with 
these should be `1-1.2.2` and `1-1.2.3` for the Arduino and Magnetometer respectively. 
The command for starting the program would then be:
```
$ python3 main.py -l '1-1.2.2' -s '1-1.2.3'
```
**Note: If you are using your own laptop to control the cage, or these bus locations provoke an 
error, please see "Connecting to the Cage Manually"**

Once the script has started you can view the various commands available using the `help` command.
![helmholtz_help](https://github.com/user-attachments/assets/d9d7023a-c39e-4fea-ba2e-20a3f53f1c34)

### Using the `set_field` command

For a quick test to see that things are operational you might begin with the `set_field` command.
This allows you to provide a target vector which the cage will attempt to produce approximately.
For instance, try:
```
> set_field 0 0 0
Setting magnetic field to target vector : 0, 0, 0
```
This will attempt to produce zero field at the location of the magnetometer by cancelling out the 
earths magnetic field in the cage. Without calibration this result will be quite inaccurate, but
you should see a change in the magnetometer readings.

**Important: In order to exit the program please use the `exit` command as this will disable the cage for you. Otherwise, some power supplies may remain active!**

---
## Testing & Analyzing Data:

This feature is yet to be implemented, but is intended to describe the open loop control of the 
cage which allow for dynamic orbital simulations to be run, as well as the calibration features 
of the cage control program.

---
## While the Helmholtz Cage is Running:

* Do not leave the cage unattended. You must monitor it constantly in case of a fire, to maintain safe temperatures for components, and to ensure accurate data collection.
* When the cage is running, do not touch or hold the red coils! They get hot and can cause injury/burns.
* Turn off the surge protector to turn the cage off for any reason.

---
## Finishing Up:

1. Once testing is completed, turn off the Raspberry Pi by issueing the `shutdown` through the console
2. Wait for the raspberry pi to shutdown completely.
3. Turn off the keyboard!! Don’t waste the batteries!
4. Flip off the surge protector to power down the power supplies, monitor, and cage.
5. If you adjusted the coil placement, wait until the red wire is cool to the touch before returning the coils to their originally labelled terminals.
6. Clean up after yourself and keep the workstation organized!
