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
              val: str) -> None:
        pass

    @abstractmethod
    def read(self,
             lba: int) -> None:
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
            for lba in range(0, 100):
                f.write(f"[{lba}] 0x{0:08X}\n")

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
              val: str) -> None:
        if not isinstance(lba, int) or not isinstance(val, str):
            raise TypeError("Please check input type. lba:int, val:str")
        if not 0 <= lba < 100:
            raise ValueError("LBA is out of range [0, 100).")
        if not len(val) == 10 or not val[:2] == "0x":
            raise ValueError("target value must be 10 digits. (ex)0x00001234")

        try:
            self._data[lba] = int(val, 16)
        except ValueError:
            raise ValueError("Val must be hex value.")
        else:
            self._update_nand()

    @overrides
    def read(self,
             lba: int) -> None:
        if not isinstance(lba, int):
            raise TypeError("LBA must be an integer.")

        if not 0 <= lba < 100:
            raise ValueError("LBA is out of range [0, 100).")

        with open(self._result_path, "w") as f:
            f.write(f'0x{self._data[lba]:08X}')


def ssd(*args):
    assert len(args) > 1, "Command line argument must be provided."

    my_ssd = SSD()

    op = args[1]
    assert op in ('R', 'W'), "Only 'R' and 'W' are supported."

    lba = int(args[2])
    if op == 'R':
        my_ssd.read(lba)

    if op == 'W':
        val = args[3]
        my_ssd.write(lba, val)


if __name__ == "__main__":
    ssd(*sys.argv)
