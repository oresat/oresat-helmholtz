# Helmholtz Shell

The Helmholtz Shell acts as an interface for the Helmholtz cage operator to issue commands
and control the system through the command line. This facilitates the interactive command line
environment using Python's cmd module. See their docs for more. The operator may manually control
the cage via calls to the Arduino, Magnetometer, and Power supplies, or by initiating simulations 
and calibration methods using the various tools provided in the utilites module.

---
## Power supply controls:

---
### `do_model(arg)`
Arguments: 
* `device_name` : char `'X'`, `'Y'`, or `'Z'` indicating axis

Return: None

Provides a command to call 'model()' from the ZXY6005s module

---
### `do_firmware(arg)`
Arguments: 
* `device_name` : char `'X'`, `'Y'`, or `'Z'` indicating axis

Return: None

Provides a command to call 'firmware_version()' from the ZXY6005s module

---
### `do_power(arg)`
Arguments: 
* `device_name` : char `'X'`, `'Y'`, or `'Z'` indicating axis
* `value` : integer `0` or `1` for `OFF` or `ON` respectively

Return: None

Provides a command to call 'set_output()' from the ZXY6005s module

---
### `do_amp_hour(arg)`
Arguments: 
* `device_name` : char `'X'`, `'Y'`, or `'Z'` indicating axis
* `value` : unsigned integer value in mAh

Return: None

Provides a command to call 'set_amp_hour()' from the ZXY6005s module

---
### `do_return_amp_hour(arg)`
Arguments: 
* `device_name` : char `'X'`, `'Y'`, or `'Z'` indicating axis

Return: None

Provides a command to call 'return_amp_hour()' from the ZXY6005s module

---
### `do_voltage(arg)`
Arguments: 
* `device_name` : char `'X'`, `'Y'`, or `'Z'` indicating axis
* `value` : unsigned integer value in mV

Return: None

Provides a command to call 'set_voltage()' from the ZXY6005s module

---
### `do_return_voltage(arg)`
Arguments: 
* `device_name` : char `'X'`, `'Y'`, or `'Z'` indicating axis

Return: None

Provides a command to call 'return_voltage()' from the ZXY6005s module

---
### `do_current_limit(arg)`
Arguments: 
* `device_name` : char `'X'`, `'Y'`, or `'Z'` indicating axis
* `value` : unsigned integer value in mA

Return: None

Provides a command to call 'set_current_limit()' from the ZXY6005s module

---
### `do_return_current(arg)`
Arguments: 
* `device_name` : char `'X'`, `'Y'`, or `'Z'` indicating axis

Return: None

Provides a command to call 'return_current_limit()' from the ZXY6005s module

---
### `do_return_mode(arg)`
Arguments: 
* `device_name` : char `'X'`, `'Y'`, or `'Z'` indicating axis

Return: None

Provides a command to call 'return_mode()' from the ZXY6005s module

---
### `do_return_temp(arg)`
Arguments: 
* `device_name` : char `'X'`, `'Y'`, or `'Z'` indicating axis

Return: None

Provides a command to call 'return_temp()' from the ZXY6005s module

---
## Arduino (H-Bridge) controls:

---
### `do_set_positive_X(arg)`
Arguments: None

Return: None

Provides a command to call `set_positive_X()` from the Arduino module. Response from the
Arduino is printed to the command line.

---
### `do_set_positive_Y(arg)`
Arguments: None

Return: None

Provides a command to call `set_positive_Y()` from the Arduino module. Response from the
Arduino is printed to the command line.

---
### `do_set_positive_Z(arg)`
Arguments: None

Return: None

Provides a command to call `set_positive_Z()` from the Arduino module. Response from the
Arduino is printed to the command line.

---
### `do_set_negative_X(arg)`
Arguments: None

Return: None

Provides a command to call `set_negative_X()` from the Arduino module. Response from the
Arduino is printed to the command line.

---
### `do_set_negative_Y(arg)`
Arguments: None

Return: None

Provides a command to call `set_negative_Y()` from the Arduino module. Response from the
Arduino is printed to the command line.

---
### `do_set_negative_Z(arg)`
Arguments: None

Return: None

Provides a command to call `set_negative_Z()` from the Arduino module. Response from the
Arduino is printed to the command line.

---
### `do_deactivate_X(arg)`
Arguments: None

Return: None

Provides a command to call `deactivate_X()` from the Arduino module. Response from the
Arduino is printed to the command line.

---
### `do_deactivate_Y(arg)`
Arguments: None

Return: None

Provides a command to call `deactivate_Y()` from the Arduino module. Response from the
Arduino is printed to the command line.

---
### `do_deactivate_Z(arg)`
Arguments: None

Return: None

Provides a command to call `deactivate_Z()` from the Arduino module. Response from the
Arduino is printed to the command line.

---
### `do_deactivate_all(arg)`
Arguments: None

Return: None

Provides a command to call `deactivate_all()` from the Arduino module. Response from the
Arduino is printed to the command line.

---
### `do_bridge_status(arg)`
Arguments: None

Return: None

Provides a command to call `get_bridge_status()` from the Arduino module. Response from the
Arduino is printed to the command line.

---
## Magnetometer Commands

---
### `do_meter_properties(arg)`
Arguments: None

Return: None

Provides a command to call `meter_properties()` from the Magnetometer module. Response from the
Arduino is printed to the command line.

---
### `do_meter_values(arg)`
Arguments: None

Return: None

Provides a command to call `meter_value_settings()` from the Magnetometer module. Response from the
Arduino is printed to the command line.

---
### `do_var_tag(arg)`
Arguments: None

Return: None

Provides a command to call `var_adc_settings()` from the Magnetometer module. Response from the
Arduino is printed to the command line.

---
### `do_stream(arg)`
Arguments: None

Return: None

Provides a command to call `stream_data()` from the Magnetometer module. Response from the
Arduino is printed to the command line.

---
## Utilites Commands:

---
### `do_calibration(arg)`
Arguments: None

Return: None

Provides a command to call `calibration()` from the Utilities module.

---
### `do_average(arg)`
Arguments: None

Return: None

Provides a command to call `reading_average()` from the Utilities module.

---
### `do_set_field(arg)`
Arguments:
* `X_mag` : desired magnetic field component in the X-axis coil
* `Y_mag` : desired magnetic field component in the Y-axis coil
* `Z_mag` : desired magnetic field component in the Z-axis coil
Must provide 3 arguments separated by spaces, e.g: set_field 10 10 10

Return: None

Provides a command to call 'set_field_vector()` from the Utilities module, and parses
command line arguments which are sent as a list.

Return: None

Provides a command to call `calibration()` from the Utilities module.

---
### `do_exit(arg)`
Arguments: None

Return: None

Powers off all power supply units and terminates the program.

