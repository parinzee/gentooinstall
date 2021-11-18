"""
This module houses commonly used components.
"""
from typing import List

from rich.table import Table as r_Table


def table(title: str, columns: list, rows: List[list]) -> r_Table:
    """
    Displays a table
    """
    colors = ["cyan", "magenta", "green", "blue", "purple", "red", "yellow", "white"]
    main_table = r_Table(title=title, title_justify="center", expand=True)
    for column, color in zip(columns, colors):
        main_table.add_column(column, justify="center", style=color)

    for row in rows:
        main_table.add_row(*row)

    return main_table
