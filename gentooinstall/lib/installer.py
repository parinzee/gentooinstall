"""
This module houses the real brains of the script
"""
import sys
from copy import deepcopy

import requests
from rich.progress import Progress
from rich.prompt import Prompt

from . import disks
from .exceptions import HardwareIncompatableError, NetworkError
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
            raise HardwareIncompatableError("Your hardware is incompatable")
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


def store_disk_scheme() -> None:
    """
    Prompt the user to select a disk and it's scheme,
    before storing scheme data in storage.
    """
    # Prompt the user to select their disk and its scheme
    selected_disk = prompt.select_disk()
    scheme_choice = prompt.select_partitioning_scheme(f"/dev/{selected_disk}")
    # Set values in storage
    storage.disk = selected_disk
    storage.part_scheme = scheme_choice
    # Store the scheme-specific data into storage
    if scheme_choice == 1:
        # Pylint thinks we can't check if a substring is in a string
        # pylint: disable=unsupported-membership-test
        if "nvme" in selected_disk:
            efi_or_bios = f"/dev/{selected_disk}p1"
            swap = f"/dev/{selected_disk}p2"
            root = f"/dev/{selected_disk}p3"
        elif "sd" in selected_disk:
            efi_or_bios = f"/dev/{selected_disk}1"
            swap = f"/dev/{selected_disk}2"
            root = f"/dev/{selected_disk}3"
        else:
            HardwareIncompatableError("HDD not supported")

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
    elif scheme_choice == 2:
        console.print(
            "[bold italic yellow]Ensure you've formatted and ran mkfs or mkswap on your partitions."
        )
        partitions = disks.partitions_in_disk(f"/dev/{selected_disk}")
        # Making copy because we will modify partitions dict
        for index, part in enumerate(deepcopy(partitions)):
            mountpoint = Prompt.ask(
                f'[green]Where to mount {part[0]}? (leave blank to not use or "swap" for swap)'
            )
            if mountpoint.lower() != "":
                partitions[index].append(mountpoint.lower())

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
    elif scheme_choice == 3:
        storage.partitions = None
    else:
        # This shouldn't be possible, since the prompt gurantees a correct
        # response. But still, just in case.
        raise ValueError("Please enter 0, 1, 2, or 3 into the prompt.")


def partition_selected_disk() -> None:
    """
    Partitions selected disk if storage.part_scheme is 1
    """
    if storage.part_scheme == 1:
        with Progress(expand=True) as progress:
            partitioning_disk = progress.add_task(
                f"[yellow]Partitioning {storage.disk}..."
            )
            progress.update(partitioning_disk, advance=40)
            if storage.partitions is None:
                raise ValueError("storage.partitions is None")
            # Spawn an fdisk instance
            fdisk = Fdisk(f"/dev/{storage.disk}")
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

            progress.update(partitioning_disk, advance=50)
            fdisk.write_changes()
            progress.update(partitioning_disk, advance=10)


def format_selected_partitions() -> None:
    """
    Formats the partitions that the installation will use.
    """
    if storage.part_scheme == 1:
        if storage.partitions is None:
            raise ValueError("storage.partitions is None")
        with Progress(expand=True) as progress:
            format_part = progress.add_task(
                "[yellow]Formatting partitions...", start=False
            )
            for partition in storage.partitions:
                disks.format_filesystem(partition["name"], partition["type"])
            progress.advance(format_part, 100)


def mount_selected_partitions() -> None:
    """
    Loops through the partitions in storage.partitions and mount them
    """
    if storage.part_scheme != 3:
        if storage.partitions is None:
            raise ValueError("storage.partitions is None")
        for partition in storage.partitions:
            disks.mount(partition["name"], "/mnt/gentoo" + partition["mountpoint"])


def execute() -> None:
    "Execute all the commands for installing Gentoo."

    # Show welcoming stuff
    display.show_welcome()
    display.show_options()

    # Run checks before starting install
    preliminary_checks()

    # Start disk partitioning
    store_disk_scheme()
    # Confirm the user's choices
    if storage.partitions is not None:
        partitions_copy = deepcopy(storage.partitions)
        # The table class can't render a dict, so we'll change
        # it into a string
        for index, partition in enumerate(storage.partitions):
            if isinstance(partition["mountpoint"], dict):
                partitions_copy[index]["mountpoint"] = str(
                    partitions_copy[index]["mountpoint"]
                )
        console.print(
            table(
                "Partitions to use",
                ["Partition", "Type", "Size", "Mountpoint"],
                disks.dict_list_to_list(partitions_copy),
                padding=True,
            )
        )
    console.print(
        "[red]We are not responsible for any damage this tool may do to your device."
    )
    confirm = Prompt.ask("[green]Proceed?[/green]", choices=["y", "n"])
    if confirm == "n":
        console.print("[red]No changes made[/red]")
        sys.exit()
    partition_selected_disk()
    format_selected_partitions()
    mount_selected_partitions()
