"""
This module houses the Hardware class used for gathering details about the hardware.
"""
import os
from pathlib import Path
from typing import List

CPUINFO = Path("/proc/cpuinfo")
MEMINFO = Path("/proc/meminfo")


def get_cpu_vendor() -> dict:
    """
    Gets the cpu vendor
    """
    cpu = {"intel": False, "amd": False}
    with CPUINFO.open(encoding="UTF-8") as file:
        for line in file:
            if "GenuineIntel" in line:
                cpu["intel"] = True
            elif "AuthenticAMD" in line:
                cpu["amd"] = True
    return cpu


def get_mem_total() -> int:
    """
    Gets total memory of device in kilobytes
    """
    memory = 0
    with MEMINFO.open(encoding="UTF-8") as file:
        memory = int(file.readline().split(":")[1].lstrip().split("kB")[0].rstrip())
    return memory


class Hardware:
    """
    Stores details about the device
    """

    # We can remove this one later when we finish the required_package
    # pylint: disable=fixme, no-self-use

    def __init__(self) -> None:
        """
        Initializes class and assigns the following:
        - self.cpu
        - self.total_ram
        - self.uefi
        """
        self.cpu = get_cpu_vendor()
        self.total_mem = get_mem_total()
        self.uefi = os.path.isdir("/sys/firmware/efi")

    def suggested_swap_size(self) -> int:
        """
        Returns the suggested swap size in gigbytes
        """
        ram_in_gigs = int(str(self.total_mem)[0])
        if ram_in_gigs <= 5:
            swap_size = ram_in_gigs * 2
        elif ram_in_gigs <= 15:
            swap_size = ram_in_gigs // 2
        else:
            swap_size = 4
        return swap_size

    def hardware_compatable(self) -> bool:
        """
        Checks compatability of the hardware
        Returns a boolean.
        """
        # pylint: disable=simplifiable-if-statement,no-else-return
        compatable = {"cpu": False, "ram": False}
        if any(self.cpu.values()):
            compatable["cpu"] = True
        if self.total_mem >= 2000000:  # Check if memory is more than 2 gigs
            compatable["ram"] = True

        # Checks if everything is true
        if all(compatable.values()):
            return True
        else:
            return False

    def required_packages(self) -> List[str]:
        """
        Returns the list of required packages based on the hardware
        """
        packagelist = ["sys-kernel/linux-firmware"]

        # TODO: More logic over here

        return packagelist


hardware = Hardware()
