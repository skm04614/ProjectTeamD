class CommandBuffer:
    FULL_SIZE = 10

    def __init__(self):
        self.__buf = []

    @property
    def get_command_list(self):
        return self.__buf[:]

    def is_full(self) -> bool:
        return len(self.__buf) == CommandBuffer.FULL_SIZE

    def add_command(self,
                    cmd: str) -> None:
        self.__buf.append(cmd)
        self.optimize_buf()

    def optimize_buf(self):
        pass

    def flush(self):
        self.__buf = []

    def search(self,
               lba: int):
        result = None
        for cmd in self.__buf:
            split_cmd = cmd.split(" ")
            if split_cmd[0] == "W" and int(split_cmd[1]) == lba:
                result = int(split_cmd[2], 16)
            elif split_cmd[0] == "E" and self.check_erase_range(lba, int(split_cmd[1]), int(split_cmd[2])):
                result = 0x00000000
        return result

    def check_erase_range(self,
                          lba: int,
                          start_lba: int,
                          size: int):
        return start_lba <= lba < start_lba + size
