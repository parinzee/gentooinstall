"""
This module houses all the exceptions.
"""
import subprocess


class NetworkError(Exception):
    """
    Exception raised when there is a generic network error.
    """


class NoNetworkError(Exception):
    """
    Exception raised when the script can't access the internet.
    """

    def __init__(self) -> None:
        self.error = """
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
        super().__init__(self.error)


class CommandError(subprocess.CalledProcessError):
    """
    Exception raised when a subprocess.run command fails.
    """

    def __init__(
        self,
        returncode: int,
        cmd,
        output=None,
        stderr=None,
    ) -> None:
        self.message = """
                        This should not happen. Please try again. 
                        If the problem persists, report the issue on github.
                        """
        super().__init__(returncode, cmd, output=output, stderr=stderr)


class HardwareIncompatableError(Exception):
    """
    Exception raised when Hardware is incompatable
    """
