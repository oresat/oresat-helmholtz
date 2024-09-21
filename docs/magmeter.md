# Magnetometer Module
The magnetometer module facilitates serial communication between the Raspberry Pi and the
magnetometer. This module includes functions which can be used to request, read, and parse
magnetometer readings and settings.

---
## `proto_read_chunk()`
Arguments: None

Return:
* `data` : bytearray of 20 bytes

Reads a single chunk (20 bytes) from the serial port.

---
## `send_command(command, extra_bytes = None)`
Arguments:
* `command` : a predefined command byte according to the magnetometer documentation
* `extra_bytes` : optional bytes to provide a buffer at the end of the command signal

Return: None

This is a helper function used to communicate with the magnetometer.

---
## `acknowledgement()`
Arguments: None

Return: None

Sends an `ack` command to the magnetometer. This is a helper function to be called at the end
of a transmission to the magnetometer.

---
## `handle_meter_response()`
Arguments: None

Return: None

This function reads a response from the magnetometer and prints the decoded message to the
console.

---
## `parse_meter_response(response)`
Arguments: None

Return: None

Reads a response from the meter as a string and creates a list of data points, which is
printed to the console.

---
## `read_stream_data()`
Arguments: None

Return:
* `chunk` : list of four data points returned by the magnetometer, stored in a dictionary
Each element in the return chunk has a dictionary structure returned by `parse_data_point()`.
See the `parse_data_point()` section of this document for more details.

Each chunk is gathered during a single transmission provided by the magnetometer, typically of the
form `[ <time>, <x reading>, <y reading>, <z reading>]`

---
## `parse_data_point(data_point, dict)`
Arguments:
* `data_point` : a bytearray provided from the magnetometer
* `dict` : a dictionary containing labels for the structure of returned data

Return:
* dict : a dictionary containing a single data point.

See the dictionary structure and table below.
```
{'config' : config_info, 'sign' : sign, 'power' : decimal_power, 'raw_value' : raw_value, 'value' : value}
```
Refer to the following table for information about each element of the dictionary.
|    key      |  type  |     element                                              |
| ---------   | ----   | -------------------------------------------------------- |
| `config`    | `int`  | config info about data point, not used                   |
| `sign`      | `int`  | either `1` or `-1` indicating the sign of the data point |
| `power`     | `int`  | power of 10 which the raw value should be divided by     |
| `raw_value` | `int`  | unsigned value of data point                             |
| `value`     | `int`  | signed data point with decimal point adjusted            |

Data returned by the magnetometer has a complicated format which requires bit-wise operations to
be readable. This function carries out these operations and returns a dictionary containing the
readable results.

---
## `meter_properties()`
Arguments: None

Return: None

This sends a request for meter properties to the magnetometer which are then printed to the
command line.

---
## `meter_value_settings()`
Arguments: None

Return: None

This sends a request for meter settings to the magnetometer which are then printed to the
command line.

---
## `var_adc_settings()`
Arguments: None

Return: None

This sends a request for analog-to-digital conversion settings to the magnetometer which are then 
printed to the command line.

---
## `stream_data()`
Arguments: None

Return:
* `chunk` : the chunk acquired through a call to `read_stream_data()`

This function sends a request for data to the magnetometer then initiates a call to
read the data coming over the serial bus. See documentation for `read_stream_data()` for
more information and the return value.
