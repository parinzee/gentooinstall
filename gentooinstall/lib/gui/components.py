"""
This module houses commonly used components.
"""
from typing import List

from rich.padding import Padding
from rich.table import Table as r_Table


def table(
    title: str, columns: list, rows: List[list], padding: bool = False
) -> r_Table:
    """
    Displays a table
    """
    colors = ["cyan", "magenta", "green", "blue", "purple", "red", "yellow", "white"]
    if padding:
        main_table = r_Table(
            title=Padding(title, (2, 0, 0, 0)),  # type: ignore[arg-type]
            title_justify="center",
            expand=True,
        )
    else:
        main_table = r_Table(
            title=title,
            title_justify="center",
            expand=True,
        )
    for column, color in zip(columns, colors):
        main_table.add_column(column, justify="center", style=color)

    for row in rows:
        main_table.add_row(*row)

    return main_table
