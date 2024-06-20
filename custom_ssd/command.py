from typing import Any

from abc import ABC, abstractmethod


class ICommand(ABC):
    def __init__(self,
                 ssd,
                 start_lba: Any,
                 end_lba: Any) -> None:
        ssd.check_lba(start_lba)
        ssd.check_lba(end_lba)

        self._ssd = ssd
        self._start_lba = int(start_lba)
        self._end_lba = int(end_lba)

    @property
    def start_lba(self) -> int:
        return self._start_lba

    @property
    def end_lba(self) -> int:
        return self._end_lba

    @abstractmethod
    def execute(self) -> None:
        pass


class WriteCommand(ICommand):
    def __init__(self,
                 ssd,
                 lba: Any,
                 val: Any) -> None:
        ssd.check_val(val)
        super().__init__(ssd, lba, lba)

        self._val = str(val)

    @property
    def val(self) -> int:
        return int(self._val, 16)

    def execute(self) -> None:
        self._ssd.update_nand_data(self._start_lba, self._val)
        self._ssd.flush_nand_data_to_path()


class ReadCommand(ICommand):
    def __init__(self,
                 ssd,
                 lba: Any) -> None:
        super().__init__(ssd, lba, lba)

    def execute(self) -> None:
        self._ssd._custom_os.write_to_memory(f"0x{self._ssd.search(self._start_lba):08X}")


class EraseCommand(ICommand):
    def __init__(self,
                 ssd,
                 lba: Any,
                 size: Any) -> None:
        ssd.check_lba(lba)
        ssd.check_erase_size(size)

        super().__init__(ssd, lba, int(lba) + int(size) - 1)

    def execute(self) -> None:
        for lba in range(self._start_lba, self._end_lba + 1):
            self._ssd.update_nand_data(lba, "0x00000000")
        self._ssd.flush_nand_data_to_path()


class FlushCommand(ICommand):
    def __init__(self,
                 ssd) -> None:
        super().__init__(ssd, ssd.LBA_LOWER_BOUND, ssd.LBA_UPPER_BOUND)

    def execute(self) -> None:
        self._ssd.flush_buffer()
