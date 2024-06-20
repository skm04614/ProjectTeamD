from typing import Optional, Iterable

from custom_ssd.command import *


class CommandBuffer:
    MAX_SIZE = 10

    def __init__(self) -> None:
        self.__commands: list[ICommand] = []

    def __iter__(self) -> Iterable[ICommand]:
        return iter(self.__commands)

    def is_full(self) -> bool:
        return len(self.__commands) >= CommandBuffer.MAX_SIZE

    def add_command(self,
                    command: ICommand) -> None:
        self.__commands.append(command)
        self.__optimize()

    def flush(self) -> None:
        for command in self.__commands:
            command.execute()
        self.__commands = []

    def search(self,
               lba: int) -> Optional[int]:
        for command in self:
            if not command.start_lba <= lba <= command.end_lba:
                continue

            if isinstance(command, WriteCommand):
                return command.val

            if isinstance(command, EraseCommand):
                return 0x0

        return None

    def __optimize(self):
        pass
