import os


class SSDWriter:
    def write(self,
              lba: int,
              val: int) -> bool:
        os.system(f"python ../ssd/ssd.py W {lba} {val}")

        return True
