# Utilities Module
Utilities hosts many complex calibration functions, helper functions, and relatively simple 
executive functions which help the operator to produce magnetic field vectors accurately.

---
## `reading_avg()`
This function uses the magnetometer `stream` function to collect readings of Earth's magnetic
field at the center of the cage and averages the result. This allows for more accurate 
reproduction of target vectors.

---
## `to_output_current(target_currents)`
Arguments:
* `target_currents` : 1-dim array or list of 3 currents derived theoretically for each axis (x, y, z)

Return:
* `out_currents` : 1-dim array of 3 currents to be used as power supply limits to produce the target

In a perfect world this function doesn't exist, but in order to produce accurate magnetic
field simulations this function uses linear-regression coefficients, which have been experimentally
determined by the Helmholtz team, to essentially *course correct* the current control operations
and provide results which are more accurate to their theoretical targets. It is recomended that 
this function is used *after* calls to `mag_to_current()` and *before* using `set_current_limit()`.

---
## `mag_to_current(target_mag, xyz_slope, ambient_mag)`
Arguments:
* `target_mag` : 1-dim array or list of 3 magnetic field components of the desired magnetic vector
* `xyz_slope` : linear coefficients derived from linear regression of magnetic-current relationship
* `ambient_mag` : linear regression coefficients or average field in the cage provided by Earth's dipole

Return:
* `target_currents` : 1-dim array of 3 current vector components which should be produced in the cage

This function uses linear regression coefficients produced by the magnetic-field-to-current 
relation which are provided by the calibration function to convert a target magnetic field vector
to a target current vector.

---
## `set_field_vector(target=[0, 0, 0], xyz_slope, ambient_field)`
Arguments:
* `target` : 1-dim array or list of 3 magnetic field components of a desired B-field vector
* `xyz_slope` : linear coefficients of magnetic-current relation
* `ambient_field` : linear coefficients or average field to be negated

Return:
* boolean :  0 if successful, -1 if error occurs

Using this function streamlines the process of producing a magnetic field vector in the cage.
Accuracy of the result depends of the accuracy of the `zyx_slope` and `ambient_field` arguments
which can be updated by calls to the calibration function.

---
## calibration()
Arguments:
None

Return:
* `(xyz_slope, ambient_field)` : tuple of linear regression coefficients resulting from magnetic-current relationship.

---
## linear_regression(x, y)
Arguments
* `x` : array of values for the independent variable
* `y` : array of values for the dependent variable

Returns:
* `(m, y_0)` : tuple of linear regression coefficients

This is a helper function which performs linear regression on a 2-dim dataset using the least 
squares method.

