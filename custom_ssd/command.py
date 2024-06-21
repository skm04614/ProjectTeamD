from typing import Any

from abc import ABC, abstractmethod


class ICommand(ABC):
    class InvalidLBARangeException(Exception):
        def __init__(self,
                     msg: str) -> None:
            super().__init__(msg)

    def __init__(self,
                 ssd: "custom_ssd.cssd.SSD",
                 start_lba: Any,
                 end_lba: Any) -> None:
        self._start_lba: int = 0
        self._end_lba: int = 0

        self._ssd = ssd
        self.set_lbas(start_lba, end_lba)

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def start_lba(self) -> int:
        return self._start_lba

    @property
    def end_lba(self) -> int:
        return self._end_lba

    @abstractmethod
    def execute(self) -> None:
        pass

    def set_lbas(self,
                 start_lba: int,
                 end_lba: int) -> None:
        self._ssd.check_lba(start_lba)
        self._ssd.check_lba(end_lba)
        self.__check_valid_lba_range()

        self._start_lba = int(start_lba)
        self._end_lba = int(end_lba)

    def is_consecutive(self,
                       other: "ICommand") -> bool:
        if not isinstance(other, self.__class__):
            return False

        return (self.start_lba == other.end_lba + 1
                or other.start_lba == self.end_lba + 1)

    def overlaps(self,
                 other: "ICommand") -> bool:
        if not isinstance(other, ICommand):
            return False

        return (other.start_lba in range(self.start_lba, self.end_lba + 1)
                or other.end_lba in range(self.start_lba, self.end_lba + 1)
                or self.start_lba in range(other.start_lba, other.end_lba + 1)
                or self.end_lba in range(other.start_lba, other.end_lba + 1))

    def __check_valid_lba_range(self) -> None:
        if self._start_lba > self._end_lba:
            raise ICommand.InvalidLBARangeException("start_lba <= end_lba is required.")


class WriteCommand(ICommand):
    def __init__(self,
                 ssd: "custom_ssd.cssd.SSD",
                 lba: Any,
                 val: Any) -> None:
        ssd.check_val(val)
        super().__init__(ssd, lba, lba)

        self._val = str(val)

    def __str__(self) -> str:
        return f"W {self._start_lba} {self._val}"

    @property
    def val(self) -> str:
        return self._val

    def execute(self) -> None:
        for lba in range(self.start_lba, self.end_lba + 1):
            self._ssd.update_nand_data(lba, self.val)
        self._ssd.flush_nand_data_to_path()


class ReadCommand(ICommand):
    def __init__(self,
                 ssd: "custom_ssd.cssd.SSD",
                 lba: Any) -> None:
        super().__init__(ssd, lba, lba)

    def __str__(self) -> str:
        return f"R {self._start_lba}"

    def execute(self) -> None:
        self._ssd.custom_os.write_to_memory(self._ssd.search(self._start_lba))


class EraseCommand(ICommand):
    def __init__(self,
                 ssd: "custom_ssd.cssd.SSD",
                 lba: Any,
                 size: Any) -> None:
        ssd.check_lba(lba)
        ssd.check_erase_size(size)
        self.__size = size

        super().__init__(ssd, lba, int(lba) + int(size) - 1)

    def __str__(self) -> str:
        return f"E {self._start_lba} {self.__size}"

    def set_lbas(self,
                 start_lba: int,
                 end_lba: int) -> None:
        super().set_lbas(start_lba, end_lba)
        size = int(end_lba) - int(start_lba) + 1
        self._ssd.check_erase_size(size)
        self.__size = size

    def execute(self) -> None:
        for lba in range(self._start_lba, self._end_lba + 1):
            self._ssd.update_nand_data(lba, "0x00000000")
        self._ssd.flush_nand_data_to_path()


class FlushCommand(ICommand):
    def __init__(self,
                 ssd: "custom_ssd.cssd.SSD") -> None:
        super().__init__(ssd, ssd.LBA_LOWER_BOUND, ssd.LBA_UPPER_BOUND)

    def __str__(self) -> str:
        return "F"

    def execute(self) -> None:
        self._ssd.flush_buffer()
