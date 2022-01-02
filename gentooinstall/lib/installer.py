"""
This module houses the real brains of the script
"""
import sys
from copy import deepcopy
from typing import Literal

import requests
from rich.progress import Progress
from rich.prompt import Prompt

from . import disks
from .exceptions import HardwareIncompatable, NetworkError
from .fdisk import Fdisk
from .general import run_command
from .gui import display, prompt
from .gui.components import table
from .gui.console import console
from .hardware import hardware
from .storage import storage


def preliminary_checks():
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


def partition_disks(choice: Literal[1, 2, 3], disk: str) -> None:
    """
    Partitions the disks based on the choices that user made:
    1 = Basic Scheme
    2 = Existing & Set mountpoints
    3 = Use the scheme mounted at /mnt/gentoo

    It will store the scheme in storage and format the drive.
    """
    # pylint: disable=too-many-branches, too-many-statements
    if choice == 1:
        # Checks the naming scheme
        if "nvme" in disk:
            efi_or_bios = f"/dev/{disk}p1"
            swap = f"/dev/{disk}p2"
            root = f"/dev/{disk}p3"
        elif "sd" in disk:
            efi_or_bios = f"/dev/{disk}1"
            swap = f"/dev/{disk}2"
            root = f"/dev/{disk}3"
        else:
            HardwareIncompatable("HDD not supported")

        # Prompts the user to select a partitioning format
        root_fs = Prompt.ask(
            "[green]What filesystem do you want to use for your root partition?[/green]",
            choices=["ext4", "btrfs", "xfs"],
        )

        # Stores the scheme in storage.
        storage.partitions = [
            {
                "name": efi_or_bios,
                # If its efi then we use vfat otherwise we use ext4
                "type": "vfat" if hardware.uefi else "ext4",
                "size": "256M",
                "mountpoint": "/boot/efi" if hardware.uefi else "/boot",
            },
            {
                "name": swap,
                "type": "swap",
                "size": f"{hardware.suggested_swap_size()}G",
                "mountpoint": "swap",
            },
            {
                "name": root,
                "type": root_fs,
                "size": "full",
                "mountpoint": "/"
                if root_fs != "btrfs"
                else {"@": "/", "@home": "/home"},
            },
        ]

        confirm = Prompt.ask("[green]Proceed?[/green]", choices=["y", "n"])
        if confirm == "n":
            console.print("[red]No changes made[/red]")
            sys.exit()

        # Spawn an fdisk instance
        fdisk = Fdisk(f"/dev/{disk}")
        if hardware.uefi:
            fdisk.create_gpt_table()
            for partition in storage.partitions:
                if partition["type"] == "swap":
                    fdisk.create_gpt_part(f"+{partition['size']}", "swap")
                else:
                    if partition["size"] != "full":
                        fdisk.create_gpt_part(f"+{partition['size']}", None)
                    else:
                        # Fdisk interprets an empty string as 'take up whole space'
                        fdisk.create_gpt_part("", None)
        else:
            fdisk.create_dos_table()
            for partition in storage.partitions:
                if partition["type"] == "swap":
                    fdisk.create_dos_part(f"+{partition['size']}", True, "swap")
                else:
                    if partition["size"] != "full":
                        fdisk.create_dos_part(f"+{partition['size']}", True, None)
                    else:
                        fdisk.create_dos_part("", True, None)
        fdisk.write_changes()
    elif choice == 2:
        # User will select own mountpoint
        console.print(
            "[bold italic yellow]Ensure that you have formatted and ran mkfs on your partitions."
        )
        partitions = disks.partitions_in_disk(disk)
        # Making copy because we will modify partitions dict
        for index, part in enumerate(deepcopy(partitions)):
            mountpoint = Prompt.ask(
                f'[green]Where to mount {part[0]}? (leave blank to not use or "swap" for swap)'
            )
            if mountpoint.lower() == "":
                partitions[index].append(None)
            else:
                partitions[index].append(mountpoint.lower())
        console.print(
            table(
                "Partitions to use",
                ["Partition", "Size", "Type", "Mountpoint"],
                partitions,
                padding=True,
            )
        )
        confirm = Prompt.ask("[green]Proceed?[/green]", choices=["y", "n"])
        if confirm == "n":
            console.print("[red]No changes made[/red]")
            sys.exit()
        else:
            # We only want the partitions that the user will use.
            partitions_to_use = list(filter(lambda x: x[3] is not None, partitions))
            # Loop over the partitions in use to create a dictionary.
            storage.partitions = []
            for partition_info in partitions_to_use:
                storage.partitions.append(
                    {
                        "name": partition_info[0],
                        "type": partition_info[2],
                        "size": partition_info[1],
                        "mountpoint": partition_info[3],
                    }
                )

    else:
        # Use whatever is mounted at /mnt/gentoo
        storage.partitions = None


def execute() -> None:
    "Execute all the commands for installing Gentoo."

    # Show welcoming stuff
    display.show_welcome()
    display.show_options()

    # Run checks before starting install
    preliminary_checks()

    # Start disk partitioning
    disk = prompt.select_disk()
    choice = prompt.select_partitioning_scheme(disk)
    # Following function will format the disk
    # and stores the choice partition scheme
    # instide storage
    partition_disks(choice, disk)
