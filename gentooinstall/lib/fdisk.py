"""
This module is a wrapper for the fdisk program using the pexpect module.
"""
from typing import Optional, Union

# pexpect doesn't have type hints
import pexpect  # type: ignore


class Fdisk:
    """
    Class that controls the fdisk instance.
    """

    def __init__(self, path_to_disk: str) -> None:
        """
        Spawns an fdisk instance on the specified disk.
        """
        self.process = pexpect.spawn(f"fdisk {path_to_disk}")
        self.process.expect("Command (m for help): ")

    def create_gpt_table(self) -> None:
        """
        Creates empty gpt table on disk.
        """
        self.process.sendline("g")
        self.process.expect("Command (m for help): ")

    def create_dos_table(self) -> None:
        """
        Creates empty dos table on disk.
        """
        self.process.sendline("o")
        self.process.expect("Command (m for help): ")

    def _select_size(self, size: str) -> None:
        """
        Accepts default partition number, default first sector,
        then selects the size of the partition.
        """
        self.process.expect(r"Partition number \(.*\): ")
        self.process.sendline("")  # Accepts default partition number
        self.process.expect(r"First sector \(.*\): ")
        self.process.sendline("")  # Accepts default first sector
        self.process.expect(r"Last sector, \+/-sectors or \+/-size{K,M,G,T,P} \(.*\): ")
        self.process.sendline(f"+{size}")

    def create_gpt_part(self, size: str, part_type: Optional[int]) -> None:
        """
        Creates a new gpt partition based on the specified params.
        - size: specifies size
        - part_type: specifies partition type using partition codes.
        Ex: create_gpt_part("8G", 19) # Creates 8GiB swap partition
        """
        self.process.sendline("n")
        self._select_size(size)
        if part_type:
            self.process.expect("Command (m for help): ")
            self.process.sendline("t")
            patterns = self.process.expect(
                [
                    r"Partition number \(.*\): ",
                    "Partition type or alias (type L to list all): ",
                ]
            )
            if patterns == 0:
                self.process.sendline("")  # Accepts default partition number
                self.process.expect("Partition type or alias (type L to list all): ")
            self.process.sendline(str(part_type))
        self.process.expect("Command (m for help): ")

    def create_dos_part(
        self, size: str, is_primary: bool, part_type: Optional[Union[str, int]]
    ) -> None:
        """
        Creates a new dos partition based on the specified params.
        - size: specifies size
        - is_primary: specified whether partition is primary or extended.
        - part_type: specifies partition type using partition codes.
        Ex: create_gpt_part("8G", True, "82") # Creates 8GiB swap partition
        """
        self.process.sendline("n")
        self.process.expect(r"Select \(.*\): ")
        self.process.sendline("p" if is_primary else "e")
        self._select_size(size)
        if part_type:
            self.process.expect("Command (m for help): ")
            self.process.sendline("t")
            patterns = self.process.expect(
                [
                    r"Partition number \(.*\): ",
                    "Hex code or alias (type L to list all): ",
                ]
            )
            if patterns == 0:
                self.process.sendline("")  # Accepts default partition number
                self.process.expect("Hex code or alias (type L to list all): ")
            self.process.sendline(str(part_type))
        self.process.expect("Command (m for help): ")

    def write_changes(self):
        """
        Write changes to disk.
        """
        self.process.sendline("w")
