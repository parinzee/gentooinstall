"""
Tests gentooinstall.lib.installer
"""

from gentooinstall.lib.hardware import Hardware
from gentooinstall.lib.installer import preliminary_checks


# Since names of function are self-explanatory
# pylint: disable=missing-function-docstring
def test_preliminary_checks():
    hardware = Hardware()
    preliminary_checks(hardware)
    assert True
