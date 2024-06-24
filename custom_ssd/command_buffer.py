from __future__ import annotations

import os
from typing import Iterable

from custom_ssd.command import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from custom_ssd.cssd import ISSD


class CommandBuffer:
    MAX_SIZE = 10

    def __init__(self,
                 master_ssd: ISSD,
                 buffer_path: str) -> None:
        self._master_ssd = master_ssd

        self.__commands: list[ICommand] = []
        self.__buffer_path: str = buffer_path
        self._load_commands_from_path()

    def __iter__(self) -> Iterable[ICommand]:
        return iter(self.__commands)

    def __len__(self) -> int:
        return len(self.__commands)

    def __getitem__(self,
                    index: int) -> ICommand:
        return self.__commands[index]

    def is_full(self) -> bool:
        return len(self) >= CommandBuffer.MAX_SIZE

    def push(self,
             new_command: ICommand) -> None:
        if not (isinstance(new_command, WriteCommand) or isinstance(new_command, EraseCommand)):
            new_command.execute()
            return

        if self.is_full():
            self.flush()

        self.__optimize_and_queue_new_command(new_command)

    def flush(self) -> None:
        for command in self:
            command.execute()

        self.__commands = []
        self._clear_commands_in_path()

    def _load_commands_from_path(self) -> None:
        if not os.path.exists(self.__buffer_path):
            with open(self.__buffer_path, "w"):
                return

        with open(self.__buffer_path, "r") as f:
            for line in f:
                self.__commands.append(self._master_ssd.command_factory(*line.strip().split()))

        self.flush()

    def _clear_commands_in_path(self) -> None:
        with open(self.__buffer_path, "w") as f:
            pass

    def __optimize_and_queue_new_command(self,
                                         new_command: ICommand) -> None:
        if isinstance(new_command, WriteCommand):
            self.__optimize_and_queue_new_write_command(new_command)
        elif isinstance(new_command, EraseCommand):
            self.__optimize_and_queue_new_erase_command(new_command)

        with open(self.__buffer_path, "w") as f:
            f.writelines(f"{str(command)}\n" for command in self)

    def __optimize_and_queue_new_write_command(self,
                                               new_command: WriteCommand) -> None:
        commands: list[ICommand] = []
        for command in self.__commands:
            if not command.start_lba <= new_command.start_lba <= command.end_lba:
                commands.append(command)
                continue

            if isinstance(command, WriteCommand):
                continue

            if isinstance(command, EraseCommand):
                try:
                    size = new_command.start_lba - command.start_lba
                    cmd = EraseCommand(self._master_ssd, command.start_lba, size)
                except:
                    pass
                else:
                    commands.append(cmd)

                try:
                    size = command.end_lba - new_command.end_lba
                    cmd = EraseCommand(self._master_ssd, new_command.end_lba + 1, size)
                except:
                    pass
                else:
                    commands.append(cmd)

        commands.append(new_command)
        self.__commands = commands

    def __optimize_and_queue_new_erase_command(self,
                                               new_command: EraseCommand) -> None:
        commands: list[ICommand] = []

        slba = new_command.start_lba
        elba = new_command.end_lba
        for command in self.__commands:
            if isinstance(command, WriteCommand) and not slba <= command.start_lba <= elba:
                commands.append(command)
                continue

            if (slba - 1 <= command.start_lba <= elba + 1
                    or slba - 1 <= command.end_lba <= elba + 1):
                slba = min(slba, command.start_lba)
                elba = max(elba, command.end_lba)
            else:
                commands.append(command)

        while slba <= elba:
            size = min(10, elba - slba + 1)
            commands.append(EraseCommand(self._master_ssd, slba, size))
            slba += size

        self.__commands = commands
