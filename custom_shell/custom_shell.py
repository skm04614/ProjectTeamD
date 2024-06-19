import os


class CustomShell:
    def session(self) -> None:
        while True:
            args = input().split()
            method = getattr(self, args[0], None)
            if callable(method):
                try:
                    if not method(*args[1:]):
                        break
                except TypeError:
                    print(f"INVALID SET OF PARAMETERS PROVIDED FOR '{method.__name__}'.")
                    print("Use 'help' to see the manual.")
            else:
                print("INVALID COMMAND")

    def ssd_command(self, cmd: str) -> None:
        os.system(cmd)

    def write(self,
              lba: int,
              val: str) -> bool:
        # lba = int(lba)

        if not (0 <= int(lba) <= 99):
            print("LBA is out of range [0, 100).")
            return True
        if not val.startswith("0x") or len(val) != 10:
            print("invalid VAL format.")
            return True

        self.ssd_command(f"python ../ssd/ssd.py W {lba} {val}")

        return True

    def read(self,
             lba: int) -> bool:
        return True

    def exit(self) -> bool:
        print("Exiting session.")
        return False

    def help(self) -> bool:
        print("write(lba, val) - writes a val on lba")
        print("read(lba)       - reads the val written on lba")
        print("exit()          - exits program")
        print("help()          - prints manual to stdout")
        print("full_write(val) - writes val to all lbas ranging from 0 to 99")
        print("full_read()     - reads all vals written on each lba ranging from 0 to 99 and prints to stdout")

        return True

    def full_write(self,
                   val: int) -> bool:
        for lba in range(0, 100):
            self.write(lba, val)

        return True

    def full_read(self) -> bool:
        for lba in range(0, 100):
            self.read(lba)

        return True


if __name__ == "__main__":
    cshell = CustomShell()
    cshell.session()
