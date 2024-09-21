# Helmholtz Shell

The Helmholtz Shell acts as an interface for the Helmholtz cage operator to issue commands
and control the system through the command line. This facilitates the interactive command line
environment using Python's cmd module. See their docs for more. The operator may manually control
the cage via calls to the Arduino, Magnetometer, and Power supplies, or by initiating simulations 
and calibration methods using the various tools provided in the utilites module.

---
## Power supply controls:

---
### do_model(arg)

---
### do_firmware(arg)

---
### do_power(arg)

---
### do_amp_hour(arg)

---
### do_return_amp_hour(arg)

---
### do_voltage(arg)

---
### do_return_voltage(arg)

---
### do_current_limit(arg)

---
### do_return_current(arg)

---
### do_return_mode(arg)

---
### do_return_temp(arg)

---
## Arduino (H-Bridge) controls:

---
### do_set_positive_X(arg)

---
### do_set_positive_Y(arg)

---
### do_set_positive_Z(arg)

---
### do_set_negative_X(arg)

---
### do_set_negative_Y(arg)

---
### do_set_negative_Z(arg)

---
### do_deactivate_X(arg)

---
### do_deactivate_Y(arg)

---
### do_deactivate_Z(arg)

---
### do_deactivate_all(arg)

---
### do_bridge_status(arg)

---
## Magnetometer Commands

---
### do_meter_properties(arg)

---
### do_meter_values(arg)

---
## do_var_tag(arg)

---
## do_stream(arg)

---
## Utilites Commands:

---
### do_calibration(arg)

---
### do_average(arg)

---
### do_set_field(arg)

---
### do_exit(arg)

