import re
import sys
import os.path
from abc import ABC
from typing import Any

from custom_operating_system.cos import CustomOS
from custom_ssd.command import *
from custom_ssd.command_buffer import CommandBuffer


class ISSD(ABC):
    LBA_LOWER_BOUND = 0
    LBA_UPPER_BOUND = 0

    MIN_ERASE_SIZE = 1
    MAX_ERASE_SIZE = 1

    NULL = "0x00000000"

    def __init__(self,
                 nand_path: str,
                 buffer_path: str,
                 custom_os: CustomOS = CustomOS()) -> None:
        self._custom_os = custom_os

        self._nand_data: list[str] = []
        self._nand_path: str = nand_path
        self._prepare_nand()

        self._command_buffer = CommandBuffer(self, buffer_path)

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

        if operation == "F":
            return FlushCommand(self, *args)

        raise AssertionError(f"user input, '{operation}', is not supported.")

    def queue_command(self,
                      command: ICommand) -> None:
        self._command_buffer.push(command)

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

        if not re.match(r"^0x[0-9A-F]{8}$", val):
            raise ValueError("val must be 10-characters long hex value starting with 0x (e.g. '0x1A2B3C4D').")

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
        self._nand_data[lba] = val

    def flush_nand_data_to_path(self) -> None:
        with open(self._nand_path, "w") as f:
            f.writelines(f"{val}\n" for val in self._nand_data)

    def _prepare_nand(self) -> None:
        if not os.path.exists(self._nand_path):
            with open(self._nand_path, "w") as f:
                f.writelines(f"{self.NULL}\n" for _ in range(self.LBA_LOWER_BOUND,
                                                             self.LBA_UPPER_BOUND + 1))

        with open(self._nand_path, "r") as f:
            self._nand_data = [line.strip() for line in f]


class SSD(ISSD):
    LBA_LOWER_BOUND = 0
    LBA_UPPER_BOUND = 99

    MIN_ERASE_SIZE = 1
    MAX_ERASE_SIZE = 10

    def __init__(self,
                 nand_path: str = os.path.join(os.path.dirname(__file__), "nand.txt"),
                 buffer_path: str = os.path.join(os.path.dirname(__file__), "buffer.txt"),
                 custom_os: CustomOS = CustomOS()) -> None:
        super().__init__(nand_path, buffer_path, custom_os)

    def search(self,
               lba: int) -> str:
        for command in self._command_buffer:
            if not command.start_lba <= lba <= command.end_lba:
                continue

            if isinstance(command, WriteCommand):
                return command.val

            if isinstance(command, EraseCommand):
                return self.NULL

        return self._nand_data[lba]


def ssd(*args):
    assert len(args) > 1, "Command line argument must be provided."

    my_ssd = SSD()  # TODO fix, it is being used as if it's a singleton
    command = my_ssd.command_factory(*args[1:])
    my_ssd.queue_command(command)


if __name__ == "__main__":
    ssd(*sys.argv)
