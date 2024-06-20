from custom_shell.command_interface import Command


class WriteCommand(Command):
    def __init__(self, receiver, lba, value):
        self._receiver = receiver
        self._lba = lba
        self._value = value

    def execute(self):
        self._receiver.write(self._lba, self._value)


class ReadCommand(Command):
    def __init__(self, receiver, lba):
        self._receiver = receiver
        self._lba = lba

    def execute(self):
        self._receiver.read(self._lba)
