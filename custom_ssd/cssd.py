import re
import sys
import os.path
from abc import ABC, abstractmethod
from collections import OrderedDict

from custom_operating_system.cos import CustomOS
from custom_ssd.command_buffer import CommandBuffer


class ISSD(ABC):
    LBA_LOWER_BOUND = 0
    LBA_UPPER_BOUND = 0

    VAL_LOWER_BOUND = 0x0
    VAL_UPPER_BOUND = 0x0

    def __init__(self,
                 nand_path: str = os.path.dirname(__file__) + "/nand.txt",
                 custom_os: CustomOS = CustomOS()) -> None:
        self._custom_os = custom_os

        self._data: OrderedDict[int, int] = OrderedDict()
        self._nand_path: str = nand_path
        self._prepare_nand_path()
        self._prepare_nand_data()

        self._buffer = CommandBuffer()

    @property
    def custom_os(self) -> CustomOS:
        return self._custom_os

    @property
    def nand_path(self) -> str:
        return self._nand_path

    @classmethod
    def check_lba(cls,
                  lba: int) -> None:
        if not isinstance(lba, int):
            raise TypeError("LBA must be an integer typed value.")

        if not cls.LBA_LOWER_BOUND <= lba <= cls.LBA_UPPER_BOUND:
            raise ValueError(f"LBA is out of range [{cls.LBA_LOWER_BOUND}, {cls.LBA_UPPER_BOUND}].")

    @classmethod
    def check_val(cls,
                  val: str) -> None:
        if not isinstance(val, str):
            raise TypeError("val must be a string typed value.")

        if not re.match(r"^0x[0-9a-fA-F]{8}$", val):
            raise ValueError("val must be 10-characters long hex value starting with 0x (e.g. '0x1A2B3C4D').")

        if not cls.VAL_LOWER_BOUND <= int(val, 16) <= cls.VAL_UPPER_BOUND:
            raise ValueError(f"val is out of range [{cls.VAL_LOWER_BOUND}, {cls.VAL_UPPER_BOUND}].")

    @abstractmethod
    def write(self,
              lba: int,
              val: str) -> None:
        pass

    @abstractmethod
    def read(self,
             lba: int) -> None:
        pass

    @abstractmethod
    def erase(self,
              start_lba: int,
              size: int) -> None:
        pass

    @abstractmethod
    def flush(self):
        pass

    def _update_nand(self) -> None:
        with open(self._nand_path, "w") as f:
            for lba, val in self._data.items():
                f.write(f"[{lba}] 0x{val:08X}\n")

    def _prepare_nand_data(self) -> None:
        pattern = re.compile(r"\[(?P<lba>\d+)]\s+(?P<val>0x[0-9a-fA-F]+)")
        with open(self._nand_path, "r") as f:
            for line in f:
                m = pattern.match(line)
                self._data[int(m["lba"])] = int(m["val"], 16)

    def _prepare_nand_path(self):
        if os.path.exists(self._nand_path):
            return

        with open(self._nand_path, "w") as f:
            for lba in range(self.__class__.LBA_LOWER_BOUND,
                             self.__class__.LBA_UPPER_BOUND + 1):
                f.write(f"[{lba}] 0x{0:08X}\n")


class SSD(ISSD):
    LBA_LOWER_BOUND = 0
    LBA_UPPER_BOUND = 99

    VAL_LOWER_BOUND = 0x0
    VAL_UPPER_BOUND = 0xFFFFFFFF

    def __init__(self,
                 nand_path: str = os.path.dirname(__file__) + "/nand.txt",
                 custom_os: CustomOS = CustomOS()) -> None:
        super().__init__(nand_path, custom_os)

    def write(self,
              lba: int,
              val: str) -> None:
        SSD.check_lba(lba)
        SSD.check_val(val)

        self._data[lba] = int(val, 16)
        self._update_nand()

    def read(self,
             lba: int) -> None:
        SSD.check_lba(lba)

        self._custom_os.write_to_memory(f"0x{self.__search(lba):08X}")

    def erase(self,
              start_lba: int,
              size: int) -> None:
        SSD.check_lba(start_lba)

        if not 0 < size <= 10:
            raise ValueError("Size is out of range (0, 10].")

        end_lba = start_lba + size - 1
        SSD.check_lba(end_lba)

        for lba in range(start_lba, end_lba + 1):
            self.write(lba, "0x00000000")

    def flush(self):
        for command in self._buffer:
            args = command.split(" ")
            if args[0] == "W":
                self.write(int(args[1]), args[2])
            elif args[0] == "E":
                self.erase(int(args[1]), int(args[2]))

        self._buffer.flush()

    def __search(self,
                 lba: int) -> int:
        val = self._buffer.search(lba)
        if val is None:
            val = self._data[lba]

        return val


def ssd(*args):
    assert len(args) > 1, "Command line argument must be provided."

    my_ssd = SSD()

    op = args[1]
    if op == "F":
        my_ssd.flush()
        return

    lba = int(args[2])
    if op == "R":
        my_ssd.read(lba)
        return

    elif op == 'W':
        val = args[3]
        my_ssd.write(lba, val)
        return

    elif op == 'E':
        size = int(args[3])
        my_ssd.erase(lba, size)
        return

    raise AssertionError(f"user input, '{op}', is not supported.")


if __name__ == "__main__":
    ssd(*sys.argv)
