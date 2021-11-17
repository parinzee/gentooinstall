"""
This module has functions which helps display things.
"""
from rich.panel import Panel
from rich.text import Text

from ..storage import storage
from .console import console


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
    if storage.args["no_info"]:
        warn("--no-info is on, will not show informative options.")
    if storage.args["no_ntp"]:
        warn("--no-ntp is on. Be sure you have set your system time correctly.")
