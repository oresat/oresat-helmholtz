import pytest
import sys

from oresat_helmholtz.cage_controller import PowerSupply
from oresat_helmholtz import utilities

def test_create_psus():
    for device in utilities.psu_devices():
        psu = PowerSupply(device)
        index = psu.index()
        assert isinstance(index, int)
