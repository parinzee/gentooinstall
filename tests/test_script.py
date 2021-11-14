"""Tests the script class in the gentooinstall script"""
import gentooinstall


# pylint: disable=missing-function-docstring
def test_check_network():
    script = gentooinstall.script.Script()
    script.check_network()
    assert True
