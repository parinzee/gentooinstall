"""
Contains commonly used helper functions
"""
import json
import subprocess
from typing import Union

from .exceptions import CommandError


def run_command(
    command: str, get_output: bool = False, return_json: bool = False
) -> Union[None, dict, str]:
    """
    Runs a command inside the shell and depending on parameters
    will return a JSON output
    """
    # First split the command into multiple parts
    command_splitted = command.split(" ")
    try:
        output = subprocess.run(
            command_splitted,
            check=True,
            capture_output=True,
            encoding="UTF-8",
        ).stdout
    except subprocess.CalledProcessError as exception:
        raise CommandError(
            exception.returncode,
            exception.cmd,
            exception.output,
            exception.stderr,
        ) from exception

    # Checks if the user wants an output (or a json one)
    if get_output:
        if return_json:
            return json.loads(output)
        return output
    return None
