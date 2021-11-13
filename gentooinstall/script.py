"""
# Script
This module houses the real brains of
this script (which is a class named **Script**).
"""
import curses  # pylint: disable=unused-import


class Script:
    """
    This class exposes methods that allow for the installation of Gentoo.
    """

    def __init__(self, stdscrn: "curses._CursesWindow") -> None:
        """
        Initializes the script and prepares for installation.
        """
        self.stdscrn = stdscrn

    def partition_device(self) -> None:
        "Allow the users to partition their device"
        raise NotImplementedError

    def get_tarball(self) -> None:
        "Allow the users to choose and download a tarball"
        raise NotImplementedError
