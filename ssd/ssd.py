import re
import sys


class SSD:
    def __init__(self,
                 ssd_name: str = "./nand.txt") -> None:
        self.__ssd_name: str = ssd_name

        self.__data: dict[int, int] = {}
        pattern = re.compile(r"\[(?P<lba>\d+)]\s+(?P<val>0x[0-9a-fA-F]+)")
        with open(self.__ssd_name, "r") as f:
            for line in f:
                m = pattern.match(line)
                self.__data[m["lba"]] = m["val"]

    def __del__(self) -> None:
        with open(self.__ssd_name, "w") as f:
            for lba, val in self.__data.items():
                f.write(f"[{lba}] {hex(val)}\n")

    def write(self,
              lba: int,
              val: int) -> None:
        # TODO: implement logic (valid lba range [0, 99], val [0x0, 0xFFFFFFFF])
        pass

    def read(self,
             lba: int) -> int:
        # TODO: implement logic (valid lba range [0, 99])
        pass


def ssd():
    assert len(sys.argv) > 1, "Command line argument must be provided."

    op = sys.argv[1]
    assert op in ('R', 'W'), "Only 'R' and 'W' are supported."

    lba = int(sys.argv[2])
    if op == 'R':
        # TODO implement logic
        pass
    else:
        val = int(sys.argv[3])
        # TODO implement logic


if __name__ == "__main__":
    ssd()
