![alt text](https://user-images.githubusercontent.com/33878769/50576984-cde2d900-0dd2-11e9-8117-1c2e21f85c7d.png)

# OreSat Helmholtz Cage: Standard Operating Procedure

## General Notes:

* Operate the cage with 4.92 max amps and 15.20 max volts to output the largest magnetic field vector.
* Theoretical magnetic field vector equation:
![alt text](https://user-images.githubusercontent.com/33878769/50580148-2381aa80-0e00-11e9-8fdd-0a406a66f1ba.png)
  * Bz is the total field produced by both square coils as a function of the axial distance z from the center of the coils
  * u0 is the permeability of free space: 4pi*10^-7 WB A^-1 m^-1
  * n is the number of turns of wire: 58 turns
  * I is the current of the wire being analyzed: user input
  * h is the distance between the coils: 
  * a is one half the side length of the structure: 
  
**Do not operate the Helmholtz Cage if the vacuum chamber is on!**

---
## Safety:

* The red coils will get hot if operated for an extended period of time at high currents. Do not touch or hold the coils when operating the cage.
* Monitor the temperature of the wires to maintain a safe operating temperature below 140°C.
* Monitor the temperature of the main power supply to operate between -25°C to 70°C.
* If the temperature begins to approach the operating limits, turn off the power supply and let the cage cool down before resuming testing.

**Do not operate the Helmholtz Cage if the vacuum chamber is on!**

---
## Prepping the Cage:

1. It is safe to put electronic devices inside and around the cage. However, they may disrupt the magnetic field and cause discrepancies in testing data. Be mindful of this and be aware of the testing space surroundings.
2. Verify that the vacuum chamber is NOT on.
3. Verify that the coils are secured in the terminal blocks and make sure they are connected to the correct terminals/power supply. No exposed or crossing wires!
4. Turn on the surge protector. This will power the raspberry pi, monitor, power supplies, and cage.
5. Let the raspberry pi boot up.
6. Turn the keyboard and the mouse on. There are spare batteries in the tote just in case.

---
## Operating the Cage Program:

TBD

---
## Testing & Analyzing Data:

TBD

---
## While the Helmholtz Cage is Running:

* Do not leave the cage unattended. You must monitor it constantly in case of a fire, to maintain safe temperatures for components, and to ensure accurate data collection.
* When the cage is running, do not touch or hold the red coils! They get hot and can cause injury/burns.
* Turn off the surge protector to turn the cage of for any reason.

---
## Finishing Up:

1. Once testing is completed, turn off the raspberry pi using the desktop menu.
2. Wait for the raspberry pi to shutdown completely.
3. Turn off the keyboard and mouse!! Don’t waste the batteries!
4. Flip off the surge protector to power down the power supplies, monitor, and cage.
5. If you adjusted the coil placement, wait until the red wire is cool to the touch before returning the coils to their originally labelled terminals.
6. Clean up after yourself and keep the workstation organized!
