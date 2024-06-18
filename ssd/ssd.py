from abc import ABC, abstractmethod
from overrides import overrides

import re
import sys


class ISSD(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def write(self,
              lba: int,
              val: int) -> None:
        pass

    @abstractmethod
    def read(self,
             lba: int) -> int:
        pass


class SSD(ISSD):
    def __init__(self,
                 ssd_name: str = "./nand.txt") -> None:
        super().__init__()
        self.__ssd_name: str = ssd_name

        self.__data: dict[int, int] = {}
        pattern = re.compile(r"\[(?P<lba>\d+)]\s+(?P<val>0x[0-9a-fA-F]+)")
        with open(self.__ssd_name, "r") as f:
            for line in f:
                m = pattern.match(line)
                self.__data[m["lba"]] = int(m["val"], 16)

    def __del__(self) -> None:
        with open(self.__ssd_name, "w") as f:
            for lba, val in self.__data.items():
                f.write(f"[{lba}] {hex(val)}\n")

    @overrides
    def write(self,
              lba: int,
              val: int) -> None:
        # TODO: implement logic (valid lba range [0, 99], val [0x0, 0xFFFFFFFF])
        pass

    @overrides
    def read(self,
             lba: int) -> int:
        # TODO: implement logic (valid lba range [0, 99])
        pass


def ssd(*args):
    assert len(args) > 1, "Command line argument must be provided."

    my_ssd = SSD()

    op = args[1]
    assert op in ('R', 'W'), "Only 'R' and 'W' are supported."

    lba = int(args[2])
    if op == 'R':
        with open("result.txt", "w") as f:
            f.write(f"{my_ssd.read(lba)}")
            return

    if op == 'W':
        val = int(args[3])
        my_ssd.write(lba, val)


if __name__ == "__main__":
    ssd(*sys.argv)
