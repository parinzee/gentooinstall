"""
This module houses the real brains of
this script (which is a class named Script).
"""
import requests
from rich.progress import Progress

from .lib.exceptions import NetworkError
from .lib.gui import display


class Script:
    # pylint: disable=no-self-use
    """
    This class exposes methods that allow for the installation of Gentoo.
    """

    def __init__(self) -> None:
        """
        Initializes the script and prepares for installation.
        """

    def check_network(self) -> None:
        """
        This function checks if we can access the internet.
        """
        try:
            # Try making request to google, if this doesn't throw an error we can proceed
            with Progress(expand=True) as progress:
                check_internet = progress.add_task(
                    "[yellow]Checking Internet...[/yellow]", start=False
                )
                requests.get("http://www.google.com", timeout=7)
                progress.start()
                progress.update(check_internet, advance=100)

        except (requests.ConnectionError, requests.Timeout) as exception:
            error = """
                Failed to access the internet. Try checking your WiFi, ethernet, or DNS settings.
                To connect to the wifi, run the following commands in your shell:

                 $ iwctl

                 [iwd]# device list 

                 # The command above will show your interface name. Use it here:
                 [iwd]# station interface_name scan

                 [iwd]# station interface_name get-networks

                 #The command above will show the wifi names. Find your wifi name & use it here:
                 [iwd]# station interface_name connect wifi_name

                 [iwd]# exit
            """
            raise NetworkError(error) from exception

    def partition_device(self) -> None:
        "Allow the users to partition their device"
        raise NotImplementedError

    def get_tarball(self) -> None:
        "Allow the users to choose and download a tarball"
        raise NotImplementedError

    def execute(self) -> None:
        "Excute all the commands"

        # Show welcoming stuff
        display.show_welcome()
        display.show_options()

        # Check for network connection
        self.check_network()

        #
