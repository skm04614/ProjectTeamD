import os
import subprocess

SSD_FILEPATH = os.path.join(os.path.dirname(__file__), "../ssd/ssd.py")
SRC_PATH = os.path.join(os.path.dirname(__file__), "../ssd/result.txt")

class SSDWriter:
    def write(self,
              lba: int,
              val: int) -> bool:
        try:
            subprocess.run(["python", SSD_FILEPATH, "W", str(lba), val],
                           check=True, text=True, timeout=15, capture_output=True)
        except subprocess.CalledProcessError:
            raise


class SSDReader:
    def read(self,
             lba: int) -> None:
        try:
            subprocess.run(["python", SSD_FILEPATH, "R", str(lba)],
                           check=True, text=True, timeout=15, capture_output=True)
        except subprocess.CalledProcessError:
            raise

        with open(SRC_PATH, "r") as f:
            print(f"{[int(lba)]} - {f.readline()}")
