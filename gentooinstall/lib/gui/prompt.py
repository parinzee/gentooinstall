"""
This module contains prompts that are used.
"""
from rich.prompt import Prompt

from ..disks import all_physical_disks


def select_disk() -> str:
    """
    This function prompts the user to select a disk.
    """
    disks_info = all_physical_disks()
    valid_choices = []
    for disk_info in disks_info:
        # Append the name of the list
        valid_choices.append(disk_info[0])
    selected = Prompt.ask(
        "[green]Please select a disk to begin partitioning:[/green]",
        choices=valid_choices,
    )
    return selected
