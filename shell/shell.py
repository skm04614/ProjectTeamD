from ssd.ssd import ISSD


class Shell:
    def __init__(self,
                 ssd: ISSD) -> None:
        self.__ssd = ssd

    def set_ssd(self,
                ssd: ISSD) -> None:
        self.__ssd = ssd

    @property
    def ssd(self) -> ISSD:
        return self.__ssd

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
        pass

    def full_write(self,
                   val: int) -> None:
        pass

    def full_read(self) -> None:
        pass
