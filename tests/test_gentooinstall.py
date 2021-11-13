"""Tests the general things about the gentooinstall script"""
import os
import subprocess

from gentooinstall import __version__


# Since names of function are self-explanatory
# pylint: disable=missing-function-docstring
def test_version():
    assert __version__ == "0.1.0"


def test_permission():
    try:
        # This should fail due to insufficient perms.
        subprocess.check_output(
            ["python3", f"{os.getcwd()}/gentooinstall"], stderr=subprocess.STDOUT
        )
        # If we get here there's somethin wrong.
        assert False
    except subprocess.CalledProcessError as error:
        # Make sure an exception is raised if script isn't running as root
        if "PermissionError: You need to be root to run this script" in str(
            error.output
        ):
            assert True
        else:
            assert False
