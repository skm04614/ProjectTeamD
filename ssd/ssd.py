import re
import sys
import os.path
from abc import ABC, abstractmethod
from overrides import overrides
from collections import OrderedDict


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
             lba: int) -> None:
        pass


class SSD(ISSD):
    def __init__(self,
                 nand_path: str = os.path.dirname(__file__) + "/nand.txt",
                 result_path: str = os.path.dirname(__file__) + "/result.txt") -> None:
        super().__init__()
        self.__nand_path: str = nand_path
        self.__result_path: str = result_path

        self.__data: OrderedDict[int, int] = OrderedDict()
        pattern = re.compile(r"\[(?P<lba>\d+)]\s+(?P<val>0x[0-9a-fA-F]+)")
        with open(self.__nand_path, "r") as f:
            for line in f:
                m = pattern.match(line)
                self.__data[int(m["lba"])] = int(m["val"], 16)

    @overrides
    def write(self,
              lba: int,
              val: int) -> None:
        # TODO: implement logic (valid lba range [0, 99], val [0x0, 0xFFFFFFFF])

        self.__update_nand()
        pass

    @overrides
    def read(self,
             lba: int) -> None:
        with open(self.__result_path, "w") as f:
            f.write(f'0x{self.__data[lba]:08x}')

    def __update_nand(self) -> None:
        with open(self.__nand_path, "w") as f:
            for lba, val in self.__data.items():
                f.write(f"[{lba}] 0x{val:08x}\n")

    @property
    def data(self) -> OrderedDict[int, int]:
        return self.__data

    @property
    def nand_path(self) -> str:
        return self.__nand_path

    @property
    def result_path(self) -> str:
        return self.__result_path


def ssd(*args):
    assert len(args) > 1, "Command line argument must be provided."

    my_ssd = SSD()

    op = args[1]
    assert op in ('R', 'W'), "Only 'R' and 'W' are supported."

    lba = int(args[2])
    if op == 'R':
        my_ssd.read(lba)

    if op == 'W':
        val = int(args[3])
        my_ssd.write(lba, val)


if __name__ == "__main__":
    ssd(*sys.argv)
