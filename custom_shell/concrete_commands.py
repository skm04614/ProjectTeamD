import os
import subprocess

SSD_FILEPATH = os.path.join(os.path.dirname(__file__), "../ssd/ssd.py")

class SSDWriter:
    def write(self,
              lba: int,
              val: int) -> bool:
        try:
            subprocess.run(["python", SSD_FILEPATH, "W", str(lba), val],
                           check=True, text=True, timeout=15, capture_output=True)
        except subprocess.CalledProcessError:
            raise
