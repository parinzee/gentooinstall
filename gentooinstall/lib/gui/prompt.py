"""
This module contains prompts that are used.
"""
import sys
from typing import Literal, cast

from rich.prompt import IntPrompt, Prompt

from ..disks import all_physical_disks
from .console import console
from .display import show_all_disks, show_disk_partitions


def select_disk():
    """
    This function prompts the user to select a disk.
    """
    show_all_disks()
    disks_info = all_physical_disks()
    valid_choices = []
    for disk_info in disks_info:
        valid_choices.append(disk_info[0])
    selected = Prompt.ask(
        "[green]Please select a disk to begin partitioning:[/green]",
        choices=valid_choices,
    )
    return selected


def select_partitioning_scheme(path_to_disk: str) -> Literal[1, 2, 3]:
    """
    This function prompts the user to select a partitioning scheme
    """
    show_disk_partitions(path_to_disk)
    console.print("[red]0: Abort Installation[/red]")
    console.print("[blue]1: Format entire drive and setup basic scheme (reccomended)")
    console.print("[yellow]2: Keep existing partitions & select mountpoints[/yellow]")
    console.print("[cyan]3: Use whatever is mounted at /mnt/gentoo[/cyan]")
    selected = IntPrompt.ask(
        "[green]Select what you want to do:[/green]", choices=["0", "1", "2", "3"]
    )

    if selected == 0:
        console.print(
            "\n[red on white]Aborted Installation, no changes made.[/red on white]"
        )
        sys.exit()

    return cast(Literal[1, 2, 3], selected)


def select_partition_format(partition: str) -> Literal["ext4", "btrfs", "xfs"]:
    """
    Prompts user to select a partition format from
    ext4, btrfs, and xfs
    """
    return cast(
        Literal["ext4", "btrfs", "xfs"],
        Prompt.ask(
            f"What filesystem do you want to use for {partition}?",
            choices=["ext4", "btrfs", "xfs"],
        ),
    )


def select_stage3() -> Literal[
    "openrc", "systemd", "desktop-openrc", "desktop-systemd"
]:
    """
    Prompts user to select the stage3 variant.
    """
    console.print(
        "Desktop profiles [bold]do not[/bold] have a desktop pre-installed.",
        style="on yellow",
    )
    console.print(
        "They simply pre-compile all the pkgs a [bold blue] non-headless install needs.",
        style="on yellow",
    )
    console.print(
        "Use these for [bold]increased installation speed[/bold].", style="on yellow"
    )
    console.print("- [blue]OpenRC[/blue] Profile")
    console.print(
        "- [blue]OpenRC[/blue] with [italic yellow]desktop[/italic yellow] Profile"
    )
    console.print("- [red]Systemd[/red] Profile")
    console.print(
        "- [red]Systemd[/red] with [italic yellow]desktop[/italic yellow] Profile"
    )
    return cast(
        Literal["openrc", "systemd", "desktop-openrc", "desktop-systemd"],
        Prompt.ask(
            "Select a stage3 type:",
            choices=["openrc", "systemd", "desktop-openrc", "desktop-systemd"],
        ),
    )
