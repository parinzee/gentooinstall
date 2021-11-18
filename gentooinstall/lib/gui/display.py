"""
This module has functions which helps display things.
"""
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from ..disks import all_physical_disks
from ..storage import storage
from .components import table
from .console import console


def display(text: str) -> None:
    """
    Prints markdown text
    """
    console.print(Markdown(text))


def warn(text: str) -> None:
    """
    Prints black text with yellow background to warn users about something.
    """
    console.print(text, justify="center", style="black on yellow")


def show_welcome() -> None:
    """
    Show the welcome text
    """
    console.clear()
    credits_text = Text(
        "Created by Parinz (Parinthapat P.)", style="bold blue", justify="center"
    )

    panel = Panel(
        credits_text,
        title="Welcome to Gentoo Install!",
    )
    console.print(panel)


def show_options() -> None:
    """
    Checks for the options that the users have enabled
    and repeat it to them.
    """
    if storage.args["no_ntp"]:
        warn("--no-ntp is on. Be sure you have set your system time correctly.")


def show_all_disks() -> None:
    """
    Shows a tables with available disks and shows
    descriptive text beside it.
    """
    message = """
# Step 1: Partitioning the disks
[Click here to view the Gentoo Handbook Section](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Disks)
"""
    disks = all_physical_disks()
    disk_table = table("", ["Name", "Size", "Label"], disks)
    display(message)
    console.print(disk_table)
