import re
import sys
import os.path
from abc import ABC, abstractmethod
from overrides import overrides
from collections import OrderedDict


class ISSD(ABC):
    def __init__(self,
                 nand_path: str = os.path.dirname(__file__) + "/nand.txt",
                 result_path: str = os.path.dirname(__file__) + "/result.txt") -> None:
        self._data: OrderedDict[int, int] = OrderedDict()
        self._nand_path: str = nand_path
        self._prepare_nand_path()
        self._prepare_nand_data()

        self._result_path: str = result_path
        self._prepare_result_path()

    @property
    def nand_path(self) -> str:
        return self._nand_path

    @property
    def result_path(self) -> str:
        return self._result_path

    @abstractmethod
    def write(self,
              lba: int,
              val: int) -> None:
        pass

    @abstractmethod
    def read(self,
             lba: int) -> None:
        pass

    def _update_nand(self) -> None:
        with open(self._nand_path, "w") as f:
            for lba, val in self._data.items():
                f.write(f"[{lba}] 0x{val:08x}\n")

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
            for lba in range(0, 100):
                f.write(f"[{lba}] 0x{0:08x}\n")

    def _prepare_result_path(self) -> None:
        with open(self._result_path, "w") as f:
            f.write("")


class SSD(ISSD):
    def __init__(self,
                 nand_path: str = os.path.dirname(__file__) + "/nand.txt",
                 result_path: str = os.path.dirname(__file__) + "/result.txt") -> None:
        super().__init__(nand_path, result_path)

    @overrides
    def write(self,
              lba: int,
              val: int) -> None:
        self.assert_invalid_input(lba, val)

        self._data[lba] = val
        self._update_nand()

    def assert_invalid_input(self,
                             lba: int,
                             val: int) -> Exception():
        if not isinstance(lba, int) or not isinstance(val, int):
            raise TypeError("LBA or val type is not integer")
        if not 0 <= lba <= 99:
            raise ValueError("LBA is out of range [0, 100).")
        if not 0x0 <= val <= 0xFFFFFFFF:
            raise ValueError("Target value is out of range [0, 0xFFFFFFFF].")
        if len(f"{val:X}") != 8:
            raise ValueError("The number of target value is not 10.")

    @overrides
    def read(self,
             lba: int) -> None:
        if not 0 <= lba < 100:
            raise ValueError("LBA is out of range [0, 100).")

        with open(self._result_path, "w") as f:
            f.write(f'0x{self._data[lba]:08x}')


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
