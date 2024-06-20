from typing import Optional, Iterable


class CommandBuffer:
    MAX_SIZE = 10

    def __init__(self) -> None:
        self.__commands: list[str] = []

    def __iter__(self) -> Iterable[str]:
        return iter(self.__commands)

    def is_full(self) -> bool:
        return len(self.__commands) == CommandBuffer.MAX_SIZE

    def add_command(self,
                    command: str) -> None:
        self.__commands.append(command)
        self.__optimize()

    def flush(self) -> None:
        self.__commands = []

    def search(self,
               lba: int) -> Optional[int]:
        for cmd in self:
            args = cmd.split(" ")

            if args[0] == "W" and int(args[1]) == lba:
                return int(args[2], 16)

            elif args[0] == "E" and self.check_erase_range(lba, int(args[1]), int(args[1]) + int(args[2])):
                return 0x00000000

        return None

    def check_erase_range(self,
                          lba: int,
                          start_lba: int,
                          end_lba: int) -> bool:
        return start_lba <= lba < end_lba

    def __optimize(self):
        pass
