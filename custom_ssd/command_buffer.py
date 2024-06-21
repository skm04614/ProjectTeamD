import copy
import os
from typing import Optional, Iterable

from custom_ssd.command import *


class CommandBuffer:
    MAX_SIZE = 10

    def __init__(self,
                 master_ssd: "custom_ssd.cssd.SSD",
                 buffer_path: str) -> None:
        self._master_ssd = master_ssd

        self.__commands: list[ICommand] = []
        self.__buffer_path: str = buffer_path
        self._load_commands_from_path()

        self._index = 0

    def __iter__(self) -> Iterable[ICommand]:
        return iter(self.__commands)

    def __len__(self) -> int:
        return len(self.__commands)

    def __getitem__(self,
                    index: int) -> ICommand:
        return self.__commands[index]

    def is_full(self) -> bool:
        return len(self.__commands) >= CommandBuffer.MAX_SIZE

    def push(self,
             new_command: ICommand) -> None:
        self.__optimize_and_queue_new_command(new_command)
        if self.is_full():
            self.flush()

    def flush(self) -> None:
        for command in self.__commands:
            command.execute()

        self.__commands = []
        self._clear_commands_in_path()

    def _load_commands_from_path(self) -> None:
        if not os.path.exists(self.__buffer_path):
            return

        with open(self.__buffer_path, "r") as f:
            for line in f:
                self.__commands.append(self._master_ssd.command_factory(line.strip().split()))

    def _clear_commands_in_path(self) -> None:
        with open(self.__buffer_path, "w") as f:
            pass

    def __optimize_and_queue_new_command(self,
                                         new_command: ICommand) -> None:
        if isinstance(new_command, WriteCommand):
            self.__optimize_and_queue_new_write_command(new_command)
        elif isinstance(new_command, EraseCommand):
            self.__optimize_and_queue_new_erase_command(new_command)
        else:
            new_command.execute()
            return

        with open(self.__buffer_path, "w") as f:
            f.writelines(f"{str(command)}\n" for command in self)

    def __optimize_and_queue_new_write_command(self,
                                               new_command: WriteCommand) -> None:
        commands: list[ICommand] = []
        for command in self.__commands:
            if not new_command.overlaps(command):
                commands.append(command)
                continue

            if isinstance(command, WriteCommand):
                continue

            if isinstance(command, EraseCommand):
                try:
                    cmd = copy.copy(command)
                    cmd.set_lbas(cmd.start_lba, new_command.start_lba - 1)
                except:
                    pass
                else:
                    commands.append(cmd)

                try:
                    cmd = copy.copy(command)
                    cmd.set_lbas(new_command.end_lba + 1, cmd.end_lba)
                except:
                    pass
                else:
                    commands.append(cmd)

        commands.append(new_command)
        self.__commands = commands

    def __optimize_and_queue_new_erase_command(self,
                                               new_command: EraseCommand) -> None:
        commands: list[ICommand] = []
        for command in self.__commands:
            if (isinstance(command, EraseCommand)
                    and (new_command.overlaps(command) or new_command.is_consecutive(command))):
                new_command.set_lbas(min(new_command.start_lba, command.start_lba),
                                     max(new_command.end_lba, command.end_lba))
            elif not new_command.overlaps(command):
                commands.append(command)

        slba = new_command.start_lba
        elba = new_command.end_lba
        while slba <= elba:
            size = min(10, elba - slba + 1)
            commands.append(EraseCommand(self._master_ssd, slba, size))
            slba += size

        self.__commands = commands
