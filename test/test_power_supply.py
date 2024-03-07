import pytest
import os

from oresat_helmholtz.psu import PSU

# TODO: dynamically find the right paths. hardcoded paths for now.
psu_tty_paths = ['/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3']

# Some small value for floating point comparisons
EPSILON = 0.000000001

@pytest.fixture(scope='module', params=psu_tty_paths)
def tty_path(request):
    yield request.param

@pytest.fixture(scope='module', params=psu_tty_paths)
def psu(request) -> PSU:
    yield PSU(request.param)

def floating_point_compare(a: float, b: float) -> bool:
    scaled_diff = (a - b) / b
    return scaled_diff < EPSILON

def test_psu_init(tty_path):
    psu = PSU(tty_path)

    # The device should not be enabled on creation
    assert not psu.enabled

def test_invalid_psu_init():
    with pytest.raises(AssertionError, match='does not exist'):
        psu = PSU('/path/does/not/exist')

def test_psu_volts_and_amps(psu):
    # It should not be possible to send messages to the PSU without having
    # enabled the device first.
    with pytest.raises(AssertionError):
        psu.voltage = 0

    with pytest.raises(AssertionError):
        psu.amperage = 0.

    psu.enable()
    assert psu.enabled

    # Ensure the volts and amps only take the appropriate types
    with pytest.raises(AssertionError):
        psu.voltage = float()

    with pytest.raises(AssertionError):
        psu.amperage = int()

    # Ensure we can get/set the volts and amps, and that types are what
    # we expect them to be.
    psu.voltage = 5
    psu.amperage = 5.

    assert psu.voltage == 5
    assert floating_point_compare(psu.amperage, 5.)

    psu.disable()
    assert not psu.enabled
