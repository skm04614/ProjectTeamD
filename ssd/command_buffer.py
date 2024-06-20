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

    def flush_buf(self):
        self.__buf = []

    def search(self, lba):
        pass
