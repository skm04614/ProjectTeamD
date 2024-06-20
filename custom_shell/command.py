import os
import subprocess

from abc import ABC, abstractmethod

from custom_operating_system.cos import CustomOS


class ICommand(ABC):
    class UnsupportedException(Exception):
        def __init__(self,
                     msg: str) -> None:
            super().__init__(msg)

    def __init__(self,
                 *args) -> None:
        self._args = args

    @abstractmethod
    def execute(self) -> None:
        pass


class WriteCommand(ICommand):
    def __init__(self,
                 *args) -> None:
        super().__init__(args)
        self._lba = int(args[0])
        self._val = str(args[1])

    def execute(self) -> None:
        try:
            subprocess.run(["python", "-m", "custom_ssd.cssd", "W", str(self._lba), self._val],
                           check=True, text=True, timeout=15, capture_output=True, encoding="UTF-8")
        except subprocess.CalledProcessError:
            raise


class FullWriteCommand(ICommand):
    def __init__(self,
                 *args) -> None:
        super().__init__(args)
        self._val = str(args[0])

    def execute(self) -> None:
        for lba in range(0, 100):
            WriteCommand(lba, self._val).execute()


class ReadCommand(ICommand):
    def __init__(self,
                 *args) -> None:
        super().__init__(args)
        self._lba = int(args[0])

    def execute(self) -> None:
        subprocess.run(["python", "-m", "custom_ssd.cssd", "R", str(self._lba)],
                       check=True, text=True, timeout=15, capture_output=True, encoding="UTF-8")

        print(f"{[int(self._lba)]} - {CustomOS().read_from_memory()}")


class FullReadCommand(ICommand):
    def execute(self) -> None:
        for lba in range(0, 100):
            ReadCommand(lba).execute()


class EraseSizeCommand(ICommand):
    def __init__(self,
                 *args) -> None:
        super().__init__(args)
        self._start_lba = int(args[0])
        self._size = int(args[1])

    def execute(self) -> None:
        EraseRangeCommand(self._start_lba,
                          self._start_lba + self._size).execute()


class EraseRangeCommand(ICommand):
    def __init__(self,
                 *args) -> None:
        super().__init__(args)
        self._start_lba = int(args[0])
        self._end_lba = int(args[1])

    def execute(self) -> None:
        slba = self._start_lba
        while slba + 10 < self._end_lba:
            subprocess.run(["python", "-m", "custom_ssd.cssd", "E", str(slba), str(10)],
                           check=True, text=True, timeout=15, capture_output=True, encoding="UTF-8")
            slba += 10

        if slba < self._end_lba:
            subprocess.run(["python", "-m", "custom_ssd.cssd", "E", str(slba), str(self._end_lba - slba)],
                           check=True, text=True, timeout=15, capture_output=True, encoding="UTF-8")


class HelpCommand(ICommand):
    def execute(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), "manual.txt"), "r") as f:
            print(f.read())


class FlushCommand(ICommand):
    def __init__(self,
                 *args) -> None:
        super().__init__(args)

    def execute(self) -> None:
        try:
            subprocess.run(["python", "-m", "custom_ssd.cssd", "F"],
                           check=True, text=True, timeout=15, capture_output=True, encoding="UTF-8")
        except subprocess.CalledProcessError:
            raise