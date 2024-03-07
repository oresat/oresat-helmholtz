import os

import serial


def write_encoded(device: serial.Serial, message: str) -> None:
    """
    Messages written to the PSU must be newline terminated and properly encoded.
    """
    assert (
        len(message) > 0
    ), "Tried to write a message of length zero '{message}' to device '{device}'"
    encoded: bytes = (message + "\n").encode()
    written: int = device.write(encoded)
    assert written == len(encoded), "Attempted write to device '{device}' failed"


def psu_serial_device_from_tty(tty_device: str) -> serial.Serial:
    """
    Configure the serial object with appropriate configuration options for the
    PSUs in the Helmholtz cage.
    """
    return serial.Serial(
        port=tty_device,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,
    )


class PSU:
    """
    Interface for interacting with one of our PSUs over serial.
    """

    VOLTS_MAGIC_STR = "Asu"
    AMPS_MAGIC_STR = "Asi"
    DISABLE_MAGIC_STR = "Aso0"
    ENABLE_MAGIC_STR = "Aso1"

    def __init__(self, tty: str):
        assert os.path.exists(tty), f"tty path '{tty}' does not exist on filesystem"
        self.serial_device = psu_serial_device_from_tty(tty)
        self._voltage = 0
        self._amperage = 0
        self._enabled = False

    # Property to disallow users from changing manually
    @property
    def enabled(self) -> bool:
        "Has the device already been enabled?"
        return self._enabled

    def enable(self):
        self._enabled = True
        write_encoded(self.serial_device, PSU.ENABLE_MAGIC_STR)

    def disable(self):
        self._enabled = False
        write_encoded(self.serial_device, PSU.DISABLE_MAGIC_STR)

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, value: int):
        assert self.enabled, "Expected device to already be enabled"
        assert isinstance(value, int), f"Expected voltage to be an int, got {type(value)}"

        self._voltage = value

        # TODO
        # In the original code, voltage is multiplied by this value. I don't
        # know why. I am keeping this here until we can verify this is correct
        # through a user manual or someone with more knowledge of the hardware.
        scaled_value = self._voltage * 100

        write_encoded(self.serial_device, f"{PSU.VOLTS_MAGIC_STR}{scaled_value}")

    @property
    def amperage(self) -> float:
        return self._amperage

    @amperage.setter
    def amperage(self, value: float):
        assert self.enabled, "Expected device to already be enabled"
        assert isinstance(value, float), f"Expected voltage to be a float, got {type(value)}"

        self._amperage = value

        # TODO
        # In the original code, amperage is multiplied by this value. I don't
        # know why. I am keeping this here until we can verify this is correct
        # through a user manual or someone with more knowledge of the hardware.
        scaled_value = self._amperage * 1000

        write_encoded(self.serial_device, f"{PSU.AMPS_MAGIC_STR}{scaled_value}")
