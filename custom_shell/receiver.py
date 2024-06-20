class Receiver:
    def write(self, lba, value):
        print(f"Writing value {value} at LBA {lba}")

    def read(self, lba):
        print(f"Reading value at LBA {lba}")

    def erase(self, start_lba, end_lba):
        print(f"Erasing from LBA {start_lba} to LBA {end_lba}")
