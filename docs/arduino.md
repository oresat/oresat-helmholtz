# Arduino Module

The Helmholtz Cage uses an Arduino Nano to control and monitor a set of three H-Bridge drivers
which determine the direction of current through each Helmholtz coil. These functions issue 
commands which are sent to a script stored on the Arudino Nano over the serial bus.


---
## `set_positive_X() -> str`
Arguments: None

Return:
* `msg` : response from the Arduino over the serial bus

Sends a char `'x'` over the serial bus to the Arduino, setting the X-Axis to 
the positive polarity.

---
## `set_positive_Y() -> str`
Arguments: None

Return:
* `msg` : response from the Arduino over the serial bus

Sends a char `'y'` over the serial bus to the Arduino, setting the Y-Axis to 
the positive polarity.

---
## `set_positive_Z() -> str`
Arguments: None

Return:
* `msg` : response from the Arduino over the serial bus

Sends a char `'z'` over the serial bus to the Arduino, setting the Z-Axis to 
the positive polarity.

---
## `set_negative_X() -> str`
Arguments: None

Return:
* `msg` : response from the Arduino over the serial bus

Sends a char `'X'` over the serial bus to the Arduino, setting the X-Axis to 
the negative polarity.

---
## `set_negative_Y() -> str`
Arguments: None

Return:
* `msg` : response from the Arduino over the serial bus

Sends a char `'Y'` over the serial bus to the Arduino, setting the Y-Axis to 
the negative polarity.

---
## `set_negative_Z() -> str`
Arguments: None

Return:
* `msg` : response from the Arduino over the serial bus

Sends a char `'Z'` over the serial bus to the Arduino, setting the Z-Axis to 
the negative polarity.

---
## `deactivate_X() -> str`
Arguments: None

Return:
* `msg` : response from the Arduino over the serial bus

Sends a char `'b'` over the serial bus to the Arduino, setting the X-Axis to 
a high-impedence or 'off' state.

---
## `deactivate_Y() -> str`
Arguments: None

Return:
* `msg` : response from the Arduino over the serial bus

Sends a char `'c'` over the serial bus to the Arduino, setting the Y-Axis to 
a high-impedence or 'off' state.

---
## `deactivate_Z() -> str`
Arguments: None

Return:
* `msg` : response from the Arduino over the serial bus

Sends a char `'d'` over the serial bus to the Arduino, setting the Z-Axis to 
a high-impedence or 'off' state.

---
## `deactivate_all() -> str`
Arguments: None

Return:
* `msg` : response from the Arduino over the serial bus

Sends a char `'a'` over the serial bus to the Arduino, setting all axes to 
a high-impedence or 'off' state.

---
## `get_bridge_status() -> str`
Arguments: None

Return:
* string formatted `"XYZ"` : each position can be {0, 1, 2} see table and example below.

| Value | Status |
| ----- | ------ |
|   0   |  `OFF` |
|   1   |  `+`   |
|   2   |  `-`   |

Example string : "012" \
This indicates that X is deactivated, Y is in positive polarity, and Z is negative polarity.


Sends a char `'s'` over the serial bus to the Arduino, prompting the Arduino to send the
H-Bridge status signal.
