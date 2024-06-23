import os
import subprocess
from typing import Any

from abc import ABC, abstractmethod

from custom_operating_system.cos import CustomOS


class ICommand(ABC):
    class UnsupportedException(Exception):
        def __init__(self,
                     msg: str) -> None:
            super().__init__(msg)

    @abstractmethod
    def execute(self) -> None:
        pass

    @staticmethod
    def _send_ssd_command(op: str,
                          *args) -> None:
        subprocess.run(f"python -m custom_ssd.cssd {op} {' '.join(str(arg) for arg in args)}",
                       shell=True, check=True, text=True, timeout=15, capture_output=True, encoding="UTF-8")


class WriteCommand(ICommand):
    def __init__(self,
                 lba: Any,
                 val: Any) -> None:
        super().__init__()

        self.__lba = lba
        self.__val = val

    def execute(self) -> None:
        ICommand._send_ssd_command("W", self.__lba, self.__val)


class FullWriteCommand(ICommand):
    def __init__(self,
                 val: Any) -> None:
        super().__init__()

        self.__val = val

    def execute(self) -> None:
        for lba in range(0, 100):
            WriteCommand(lba, self.__val).execute()


class ReadCommand(ICommand):
    def __init__(self,
                 lba: Any) -> None:
        super().__init__()

        self.__lba = lba

    def execute(self) -> None:
        ICommand._send_ssd_command("R", self.__lba)
        print(f"[{self.__lba}] - {CustomOS().read_from_memory()}")


class FullReadCommand(ICommand):
    def execute(self) -> None:
        for lba in range(0, 100):
            ReadCommand(lba).execute()


class EraseSizeCommand(ICommand):
    def __init__(self,
                 start_lba: Any,
                 size: Any) -> None:
        super().__init__()

        self.__start_lba = int(start_lba)
        self.__end_lba = self.__start_lba + int(size)

    def execute(self) -> None:
        EraseRangeCommand(self.__start_lba, self.__end_lba).execute()


class EraseRangeCommand(ICommand):
    def __init__(self,
                 start_lba: Any,
                 end_lba: Any) -> None:
        super().__init__()

        self.__start_lba = int(start_lba)
        self.__end_lba = int(end_lba) - 1  # end_lba is not to be erased

    def execute(self) -> None:
        while self.__start_lba <= self.__end_lba:
            size = min(10, self.__end_lba - self.__start_lba + 1)
            ICommand._send_ssd_command("E", self.__start_lba, size)
            self.__start_lba += size


class HelpCommand(ICommand):
    def execute(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), "manual.txt"), "r") as f:
            print(f.read())


class FlushCommand(ICommand):
    def execute(self) -> None:
        ICommand._send_ssd_command("F")


__all__ = ("ICommand",
           "WriteCommand",
           "FullWriteCommand",
           "ReadCommand",
           "FullReadCommand",
           "EraseSizeCommand",
           "EraseRangeCommand",
           "HelpCommand",
           "FlushCommand")
