"""
This module houses the real brains of
this script (which is a class named Script).
"""
import requests
from rich.progress import Progress

from .exceptions import HardwareIncompatable, NetworkError
from .general import run_command
from .gui import display, prompt
from .hardware import Hardware
from .storage import storage


def preliminary_checks(hardware: Hardware):
    """
    This function does the following:
    - Check for minimum hardware requirements
    - Check for internet access
    - Set system time
    """
    with Progress(expand=True) as progress:
        # Check hardware for minimum requirements
        check_hardware_compat = progress.add_task(
            "[yellow]Gathering information about hardware...[/yellow]"
        )
        progress.update(check_hardware_compat, advance=50)
        if not hardware.hardware_compatable():
            raise HardwareIncompatable("Your hardware is incompatable")
        progress.update(check_hardware_compat, advance=50)

        # Check for internet access
        try:
            # Try making request to google, if this doesn't throw an error we can proceed
            check_internet = progress.add_task("[yellow]Checking Internet...[/yellow]")
            progress.update(check_internet, advance=50)
            requests.get("http://www.gooogle.com", timeout=7)
            progress.update(check_internet, advance=50)
        except (requests.ConnectionError, requests.Timeout) as exception:
            raise NetworkError from exception

        # Set system time using ntp
        if not storage.args["no_ntp"]:
            set_system_time_ntp = progress.add_task(
                "[yellow]Syncing system time with NTP...[/yellow]"
            )
            progress.update(set_system_time_ntp, advance=50)
            run_command("timedatectl set-ntp true")
            progress.update(set_system_time_ntp, advance=50)


def execute() -> None:
    "Execute all the commands for installing Gentoo."

    # Show welcoming stuff
    display.show_welcome()
    display.show_options()

    # Run checks before starting install
    hardware = Hardware()
    preliminary_checks(hardware)

    # Start disk partitioning
    display.show_all_disks()
    disk = prompt.select_disk()  # pylint: disable=unused-variable
