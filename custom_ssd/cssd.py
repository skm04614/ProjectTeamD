import re
import sys
import os.path
from typing import Any
from abc import ABC, abstractmethod
from collections import OrderedDict

from custom_operating_system.cos import CustomOS
from custom_ssd.command import *
from custom_ssd.command_buffer import CommandBuffer


class ISSD(ABC):
    LBA_LOWER_BOUND = 0
    LBA_UPPER_BOUND = 0

    VAL_LOWER_BOUND = 0x0
    VAL_UPPER_BOUND = 0x0

    MIN_ERASE_SIZE = 1
    MAX_ERASE_SIZE = 1

    def __init__(self,
                 nand_path: str = os.path.dirname(__file__) + "/nand.txt",
                 custom_os: CustomOS = CustomOS()) -> None:
        self._custom_os = custom_os

        self._nand_data: OrderedDict[int, int] = OrderedDict()
        self._nand_path: str = nand_path
        self._prepare_nand()

        self._command_buffer = CommandBuffer()

    @property
    def custom_os(self) -> CustomOS:
        return self._custom_os

    @property
    def nand_path(self) -> str:
        return self._nand_path

    def command_factory(self,
                        operation: str,
                        *args) -> ICommand:
        if operation == "R":
            return ReadCommand(self, *args)

        if operation == "W":
            return WriteCommand(self, *args)

        if operation == "E":
            return EraseCommand(self, *args)

        raise AssertionError(f"user input, '{operation}', is not supported.")

    def add_command(self,
                    command: ICommand) -> None:
        self._command_buffer.add_command(command)

    @classmethod
    def check_lba(cls,
                  lba: Any) -> None:
        try:
            lba = int(lba)
        except (ValueError, TypeError):
            raise TypeError("LBA must be an integer convertible value.")

        if not cls.LBA_LOWER_BOUND <= lba <= cls.LBA_UPPER_BOUND:
            raise ValueError(f"LBA is out of range [{cls.LBA_LOWER_BOUND}, {cls.LBA_UPPER_BOUND}].")

    @classmethod
    def check_val(cls,
                  val: Any) -> None:
        try:
            val = str(val)
        except (ValueError, TypeError):
            raise TypeError("val must be an string convertible value.")

        if not re.match(r"^0x[0-9a-fA-F]{8}$", val):
            raise ValueError("val must be 10-characters long hex value starting with 0x (e.g. '0x1A2B3C4D').")

        if not cls.VAL_LOWER_BOUND <= int(val, 16) <= cls.VAL_UPPER_BOUND:
            raise ValueError(f"val is out of range [{cls.VAL_LOWER_BOUND}, {cls.VAL_UPPER_BOUND}].")

    @classmethod
    def check_erase_size(cls,
                         size: Any) -> None:
        try:
            size = int(size)
        except (ValueError, TypeError):
            raise TypeError("erase size must be an integer convertible value.")

        if not cls.MIN_ERASE_SIZE <= size <= cls.MAX_ERASE_SIZE:
            raise ValueError(f"Size is out of range [{cls.MIN_ERASE_SIZE}, {cls.MAX_ERASE_SIZE}].")

    def flush_buffer(self):
        self._command_buffer.flush()

    def update_nand_data(self,
                         lba: int,
                         val: str) -> None:
        self.check_lba(lba)
        self.check_val(val)
        self._nand_data[lba] = int(val, 16)

    def flush_nand_data_to_path(self) -> None:
        with open(self._nand_path, "w") as f:
            f.writelines(f"[{lba}] 0x{val:08X}\n" for lba, val in self._nand_data.items())

    def _prepare_nand(self) -> None:
        if not os.path.exists(self._nand_path):
            with open(self._nand_path, "w") as f:
                f.writelines(f"[{lba}] 0x{0:08X}\n" for lba in range(self.__class__.LBA_LOWER_BOUND,
                                                                     self.__class__.LBA_UPPER_BOUND + 1))

        pattern = re.compile(r"\[(?P<lba>\d+)]\s+(?P<val>0x[0-9a-fA-F]+)")
        with open(self._nand_path, "r") as f:
            for line in f:
                m = pattern.match(line)
                self._nand_data[int(m["lba"])] = int(m["val"], 16)


class SSD(ISSD):
    LBA_LOWER_BOUND = 0
    LBA_UPPER_BOUND = 99

    VAL_LOWER_BOUND = 0x0
    VAL_UPPER_BOUND = 0xFFFFFFFF

    MIN_ERASE_SIZE = 1
    MAX_ERASE_SIZE = 10

    def __init__(self,
                 nand_path: str = os.path.dirname(__file__) + "/nand.txt",
                 custom_os: CustomOS = CustomOS()) -> None:
        super().__init__(nand_path, custom_os)

    def search(self,
               lba: int) -> int:
        val = self._command_buffer.search(lba)
        if val is None:
            val = self._nand_data[lba]

        return val


def ssd(*args):
    assert len(args) > 1, "Command line argument must be provided."

    my_ssd = SSD()  # TODO fix, it is being used as if it's a singleton
    my_ssd.command_factory(*args[1:]).execute()


if __name__ == "__main__":
    ssd(*sys.argv)
