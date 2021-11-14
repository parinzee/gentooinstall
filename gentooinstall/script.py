"""
# Script
This module houses the real brains of
this script (which is a class named **Script**).
"""
from .lib.storage import storage


class Script:
    """
    This class exposes methods that allow for the installation of Gentoo.
    """

    def __init__(self) -> None:
        """
        Initializes the script and prepares for installation.
        """
        self.show_info = not storage["args"].no_info  # pylint: disable=no-member

    def partition_device(self) -> None:
        "Allow the users to partition their device"
        raise NotImplementedError

    def get_tarball(self) -> None:
        "Allow the users to choose and download a tarball"
        raise NotImplementedError

    def execute(self) -> None:
        "Excute all the commands"
