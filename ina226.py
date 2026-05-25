"""
circuitpython driver for the INA226 current sensor.
"""

import time

from micropython import const

# Bits
_READ = const(0x01)

# Config Register (R/W)
_REG_CONFIG = const(0x00)
_CONFIG_RESET = const(0x8000)  # Reset Bit
# Constant bits - don't change
_CONFIG_CONST_BITS = const(0x4000)
# Averaging mode
_CONFIG_AVGMODE_MASK = const(0x0E00)
_CONFIG_AVGMODE_1SAMPLES = const(0x0000)
_CONFIG_AVGMODE_4SAMPLES = const(0x0200)
_CONFIG_AVGMODE_16SAMPLES = const(0x0400)
_CONFIG_AVGMODE_64SAMPLES = const(0x0600)
_CONFIG_AVGMODE_128SAMPLES = const(0x0800)
_CONFIG_AVGMODE_256SAMPLES = const(0x0A00)
_CONFIG_AVGMODE_512SAMPLES = const(0x0C00)
_CONFIG_AVGMODE_1024SAMPLES = const(0x0E00)

# Bus voltage conversion time
_CONFIG_VBUSCT_MASK = const(0x01C0)
_CONFIG_VBUSCT_140us = const(0x0000)
_CONFIG_VBUSCT_204us = const(0x0040)
_CONFIG_VBUSCT_332us = const(0x0080)
_CONFIG_VBUSCT_588us = const(0x00C0)
_CONFIG_VBUSCT_1100us = const(0x0100)
_CONFIG_VBUSCT_21116us = const(0x0140)
_CONFIG_VBUSCT_4156us = const(0x0180)
_CONFIG_AVGMODE_8244us = const(0x01C0)

# Shunt voltage conversion time
_CONFIG_VSHUNTCT_MASK = const(0x0038)
_CONFIG_VSHUNTCT_140us = const(0x0000)
_CONFIG_VSHUNTCT_204us = const(0x0008)
_CONFIG_VSHUNTCT_332us = const(0x0010)
_CONFIG_VSHUNTCT_588us = const(0x0018)
_CONFIG_VSHUNTCT_1100us = const(0x0020)
_CONFIG_VSHUNTCT_21116us = const(0x0028)
_CONFIG_VSHUNTCT_4156us = const(0x0030)
_CONFIG_VSHUNTCT_8244us = const(0x0038)

# Operating mode
_CONFIG_MODE_MASK = const(0x0007)  # Operating Mode Mask
_CONFIG_MODE_POWERDOWN = const(0x0000)
_CONFIG_MODE_SVOLT_TRIGGERED = const(0x0001)
_CONFIG_MODE_BVOLT_TRIGGERED = const(0x0002)
_CONFIG_MODE_SANDBVOLT_TRIGGERED = const(0x0003)
_CONFIG_MODE_ADCOFF = const(0x0004)
_CONFIG_MODE_SVOLT_CONTINUOUS = const(0x0005)
_CONFIG_MODE_BVOLT_CONTINUOUS = const(0x0006)
_CONFIG_MODE_SANDBVOLT_CONTINUOUS = const(0x0007)

# SHUNT VOLTAGE REGISTER (R)
_REG_SHUNTVOLTAGE = const(0x01)

# BUS VOLTAGE REGISTER (R)
_REG_BUSVOLTAGE = const(0x02)

# POWER REGISTER (R)
_REG_POWER = const(0x03)

# CURRENT REGISTER (R)
_REG_CURRENT = const(0x04)

# CALIBRATION REGISTER (R/W)
_REG_CALIBRATION = const(0x05)

# Mask Enable
_REG_ME = const(0x06)

# CVRF
_CVRF_MASK = const(0x01 << 3)


def _to_signed(num):
    if num > 0x7FFF:
        num -= 0x10000
    return num


class INA226:
    """Driver for the INA226 current sensor"""

    def __init__(self, i2c_device, addr=0x40, logger=None):
        self.i2c_device = i2c_device
        self.i2c_addr = addr
        self.config = 0
        self.logger = logger

        self.write_buf = bytearray(3)
        self.read_buf = bytearray(2)

        # Multiplier in mA used to determine current from raw reading
        self._current_lsb = 0

        # Multiplier in W used to determine power from raw reading
        self._power_lsb = 0

        # Set chip to known config values to start
        self._cal_value = 4096
        self.set_calibration()

    def _write_register(self, reg, value):
        while not self.i2c_device.try_lock():
            pass
        self.write_buf[0] = reg & 0xFF
        self.write_buf[1] = (value >> 8) & 0xFF
        self.write_buf[2] = value & 0xFF
        self.i2c_device.writeto(self.i2c_addr, self.write_buf)
        self.i2c_device.unlock()

    def _read_register(self, reg):
        while not self.i2c_device.try_lock():
            pass
        self.i2c_device.writeto_then_readfrom(self.i2c_addr, bytes([reg]), self.read_buf)
        self.i2c_device.unlock()
        return (self.read_buf[0] << 8) | (self.read_buf[1])

    def _trigger_oneshot_conversion(self):
        # Datasheet 6.3.1: In triggered mode, writing any of the triggered convert
        # modes into the Configuration Register (00h) triggers a single-shot conversion
        self._write_register(_REG_CONFIG, self.config)
        while not self._get_conversion_status():
            time.sleep(0.001)

    def _get_conversion_status(self):
        me = self._read_register(_REG_ME)
        return me & _CVRF_MASK

    @property
    def shunt_voltage(self):
        """The shunt voltage (between V+ and V-) in Volts (so +-.327V)"""
        value = _to_signed(self._read_register(_REG_SHUNTVOLTAGE))
        # The least signficant bit is 10uV which is 0.00001 volts
        return value * 0.00001

    @property
    def bus_voltage(self):
        """The bus voltage (between V- and GND) in Volts"""
        self._trigger_oneshot_conversion()
        raw_voltage = self._read_register(_REG_BUSVOLTAGE)
        # voltage in millVolt is register content multiplied with 1.25mV/bit
        voltage_mv = raw_voltage * 1.25
        # Return Volts instead of milliVolts
        return voltage_mv * 0.001

    @property
    def current(self):
        """The current through the shunt resistor in milliamps."""
        self._trigger_oneshot_conversion()
        read = self._read_register(_REG_CURRENT)
        raw_current = _to_signed(read)
        return raw_current * self._current_lsb

    @property
    def power(self):
        self._trigger_oneshot_conversion()
        # INA226 stores the calculated power in this register
        raw_power = _to_signed(self._read_register(_REG_POWER))
        # Calculated power is derived by multiplying raw power value with the power LSB
        return raw_power * self._power_lsb

    # Example calculations for calibration register value, current LSB and power LSB
    # 1. Assuming a 100milliOhm resistor as shunt
    # RSHUNT = 0.1
    #
    # 2. Determine current_lsb
    # Assuming a maximum expected current of 3.6A
    # current_lsb = MaxExpected_I / (2^15)
    # current_lsb = 3.6A / (2^15)
    # current_lsb = 0.0001098632813
    # -> Rounding to "nicer" numbers:
    # current_lsb = 0.0001
    #
    # 3. Setting the power LSB
    # power_lsb = 25 * current_lsb
    # power_lsb = 25 * 0.0001
    # power_lsb = 0.0025
    #
    # 4. Determine calibration register value
    # cal_value = 0.00512 / (RSHUNT * current_lsb)
    # cal_value = 0.00512 / (0.1 * 0.0001)
    # cal_value = 512
    #

    def set_calibration(self):
        """
        We expect a max current of 2A
        RSHUNT = 0.1 Ohms
        """
        self._current_lsb = 2.0 / (2.0**15)
        self._cal_value = int(0.00512 / (0.1 * self._current_lsb))
        self._power_lsb = 25.0 * self._current_lsb

        self._write_register(_REG_CALIBRATION, self._cal_value)

        config = (
            _CONFIG_CONST_BITS
            | _CONFIG_AVGMODE_1SAMPLES
            | _CONFIG_VBUSCT_588us
            | _CONFIG_VSHUNTCT_588us
            | _CONFIG_MODE_SANDBVOLT_TRIGGERED
        )

        self.config = config

        self._write_register(_REG_CONFIG, config)
