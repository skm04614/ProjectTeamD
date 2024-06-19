from custom_shell.command import Command


class WriteCommand(Command):
    def __init__(self, receiver, lba, value):
        self._receiver = receiver
        self._lba = lba
        self._value = value

    def execute(self):
        self._receiver.write(self._lba, self._value)
