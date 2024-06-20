from custom_shell.command_interface import ICommand
from custom_shell.concrete_commands import SSDWriter, SSDReader, SSDEraser


class WriteCommand(ICommand):
    def __init__(self, lba: int, value: int):
        self._receiver = SSDWriter()
        self._lba = lba
        self._value = value

    def execute(self):
        self._receiver.write(self._lba, self._value)


class ReadCommand(ICommand):
    def __init__(self, lba: int):
        self._receiver = SSDReader()
        self._lba = lba

    def execute(self):
        self._receiver.read(self._lba)


class EraseCommand(ICommand):
    def __init__(self, start_lba: int, end_lba: int):
        self._receiver = SSDEraser()
        self._start_lba = start_lba
        self._end_lba = end_lba

    def execute(self):
        self._receiver.erase_range(self._start_lba, self._end_lba)
