from util import Singleton


class CommandBuffer(metaclass=Singleton):
    def __init__(self):
        self.__buf = []

    def is_full(self) -> bool:
        return len(self.__buf) == 10

    def add(self,
            cmd: str) -> None:
        self.__buf.append(cmd)
        self.optimize_buf()

    def optimize_buf(self):
        pass

    def get_command_list(self):
        return self.__buf

    def flush_buf(self):
        self.__buf = []
