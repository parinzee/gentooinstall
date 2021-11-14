"""Gentoo Installer"""
import os
import sys

# This is done so we can import the next line
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import gentooinstall  # pylint: disable=wrong-import-position


# pylint: disable-next=no-member
def main() -> None:
    """
    Provides an entry point into the gentoo installer
    """
    # Run main app
    script = gentooinstall.Script()
    script.execute()


if __name__ == "__main__":
    # Before running the app check if we have root permissions.
    if os.geteuid() != 0:
        raise PermissionError("You need to be root to run this script")
