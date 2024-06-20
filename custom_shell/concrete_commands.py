import os
import subprocess

_SSD_FILEPATH = os.path.join(os.path.dirname(__file__), "../ssd/ssd.py")
_SRC_PATH = os.path.join(os.path.dirname(__file__), "../ssd/result.txt")


class SSDWriter:
    def write(self,
              lba: int,
              val: int) -> bool:
        try:
            subprocess.run(["python", _SSD_FILEPATH, "W", str(lba), val],
                           check=True, text=True, timeout=15, capture_output=True)
        except subprocess.CalledProcessError:
            raise


class SSDReader:
    def read(self,
             lba: int) -> None:
        try:
            subprocess.run(["python", _SSD_FILEPATH, "R", str(lba)],
                           check=True, text=True, timeout=15, capture_output=True)
        except subprocess.CalledProcessError:
            raise

        with open(_SRC_PATH, "r") as f:
            print(f"{[int(lba)]} - {f.readline()}")


class SSDEraser:
    def erase_range(self,
                    start_lba: int,
                    end_lba: int) -> None:
        slba = start_lba
        while slba + 10 < end_lba:
            subprocess.run(["python", _SSD_FILEPATH, "E", str(slba), str(10)],
                           check=True, text=True, timeout=15, capture_output=True)
            slba += 10

        if slba < end_lba:
            subprocess.run(["python", _SSD_FILEPATH, "E", str(slba), str(end_lba - slba + 1)],
                           check=True, text=True, timeout=15, capture_output=True)
