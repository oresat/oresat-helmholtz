# ZXY6005s (Power Supply Module)

In order to view and change power supply settings this module issues commands through the
serial bus which are defined by the firmware of the ZXY6005 buck converters.

---
## `model(device_name: str) -> str`
Arguments:
* `device_name` : char or str, either `'X'`, `'Y'`, or `'Z'` indicating desired axis

Return:
* `msg` : message received by the buck converter

Instructs the requested axis to send its model number over the serial bus, which is printed to
the command line.

---
## `firmware_version(device_name: str) -> str`
Arguments:
* `device_name` : char or str, either `'X'`, `'Y'`, or `'Z'` indicating desired axis

Return:
* `msg` : message received by the buck converter

Instructs the requested axis to send its firmware version over the serial bus, which is printed to
the command line.

---
## `set_output(device_name: str, value: bool) -> str`
Arguments:
* `device_name` : char or str, either `'X'`, `'Y'`, or `'Z'` indicating desired axis
* `value` : either `0` or `1`, indicating `OFF` or `ON` respectively

Return:
* `msg` : message received by the buck converter

Instructs the requested axis to either enable or disable it's output, allowing the operator to 
turn the buck converter units on and off.

---
## `set_amp_hour(device_name: str, value: int) -> str`
Arguments:
* `device_name` : char or str, either `'X'`, `'Y'`, or `'Z'` indicating desired axis
* `value` : magnitude in mAh of the desired power limitation

Return:
* `msg` : message received by the buck converter

Instructs the requested axis to set its amp-hour limitation to `value`.

---
## `return_amp_hour(device_name: str) -> int`
Arguments:
* `device_name` : char or str, either `'X'`, `'Y'`, or `'Z'` indicating desired axis

Return:
* `msg` : message received by the buck converter

Instructs the requested axis to send its maximum amp-hour limitation over the serial bus,
which is then printed to the command line.

---
## `set_voltage(device_name: str, value: int)`
Arguments:
* `device_name` : char or str, either `'X'`, `'Y'`, or `'Z'` indicating desired axis
* `value` : magnitude in mV of the desired voltage limit

Return:
* `msg` : message received by the buck converter

Instructs the requested axis to set its maximum voltage setting to `value`. 
**It is recommended that this stays at 10V!**

---
## `return_voltage(device_name: str) -> int`
Arguments:
* `device_name` : char or str, either `'X'`, `'Y'`, or `'Z'` indicating desired axis

Return:
* `msg` : message received by the buck converter

Instructs the requested axis to send its maximum voltage limitation over the serial bus,
which is then printed to the command line.

---
## `set_current_limit(device_name: str, value: int)`
Arguments:
* `device_name` : char or str, either `'X'`, `'Y'`, or `'Z'` indicating desired axis
* `value` : magnitude in mA of the desired voltage limit

Return:
* `msg` : message received by the buck converter

Instructs the requested axis to set its maximum current output to `value`. This is what is used
to manipulate the magnetic fields!

---
## `return_current(device_name: str) -> int`
Arguments:
* `device_name` : char or str, either `'X'`, `'Y'`, or `'Z'` indicating desired axis

Return:
* `msg` : message received by the buck converter

Instructs the requested axis to return its maximum current limitation over the serial bus,
which is then printed to the command line.
**Note: This value has been proven to be inaccurate by the Helmholtz team! Estimated error is
around 30mA.**

---
## `return_mode(device_name: str) -> str`
Arguments:
* `device_name` : char or str, either `'X'`, `'Y'`, or `'Z'` indicating desired axis

Return:
* `msg` : message received by the buck converter

Instructs the requested axis to send its set mode over the serial bus, which is then printed
to the command line. The possible modes are `"CC"`, or 'constant current, or `"CV"`, or 
constant voltage.

---
## `return_temp(device_name: str) -> int`
Arguments:
* `device_name` : char or str, either `'X'`, `'Y'`, or `'Z'` indicating desired axis

Return:
* `msg` : message received by the buck converter

Instructs the requested axis to send its measured temperature over the serial bus,
which is then printed to the command line. This feature has not been explored by
the Helmholtz team as of Sep. 2024, so use it with the caution that accuracy has not been
confirmed.

