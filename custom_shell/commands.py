import os
import subprocess

from abc import ABC, abstractmethod

_SSD_FILEPATH = os.path.join(os.path.dirname(__file__), "../ssd/ssd.py")
_SRC_PATH = os.path.join(os.path.dirname(__file__), "../ssd/result.txt")


class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class WriteCommand(ICommand):
    def __init__(self, lba: int, value: str) -> None:
        super().__init__()
        self._lba = lba
        self._value = value

    def execute(self) -> None:
        try:
            subprocess.run(["python", _SSD_FILEPATH, "W", str(self._lba), self._value],
                           check=True, text=True, timeout=15, capture_output=True)
        except subprocess.CalledProcessError:
            raise


class ReadCommand(ICommand):
    def __init__(self, lba: int) -> None:
        super().__init__()
        self._lba = lba

    def execute(self) -> None:
        try:
            subprocess.run(["python", _SSD_FILEPATH, "R", str(self._lba)],
                           check=True, text=True, timeout=15, capture_output=True)
        except subprocess.CalledProcessError:
            raise

        with open(_SRC_PATH, "r") as f:
            print(f"{[int(self._lba)]} - {f.readline()}")


class EraseCommand(ICommand):
    def __init__(self, start_lba: int, end_lba: int) -> None:
        super().__init__()
        self._start_lba = start_lba
        self._end_lba = end_lba

    def execute(self) -> None:
        slba = self._start_lba
        while slba + 10 < self._end_lba:
            subprocess.run(["python", _SSD_FILEPATH, "E", str(slba), str(10)],
                           check=True, text=True, timeout=15, capture_output=True)
            slba += 10

        if slba < self._end_lba:
            subprocess.run(["python", _SSD_FILEPATH, "E", str(slba), str(self._end_lba - slba + 1)],
                           check=True, text=True, timeout=15, capture_output=True)


def invoke_command(command: ICommand) -> None:
    command.execute()
