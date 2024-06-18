class CustomShell:
    def write(self,
              lba: int,
              val: int) -> None:
        pass

    def read(self,
             lba: int) -> int:
        pass

    def exit(self) -> None:
        pass

    def help(self) -> None:
        print("write(lba, val) - writes a val on lba")
        print("read(lba)       - reads the val written on lba")
        print("exit()          - exits program")
        print("help()          - prints manual to stdout")
        print("full_write(val) - writes val to all lbas ranging from 0 to 99")
        print("full_read()     - reads all vals written on each lba ranging from 0 to 99 and prints to stdout")

    def full_write(self,
                   val: int) -> None:
        pass

    def full_read(self) -> None:
        pass
