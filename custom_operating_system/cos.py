import os
import threading
from abc import ABC, abstractmethod
from typing import Any

from util import ABCSingleton


class IOS(ABC, metaclass=ABCSingleton):
    MEMORY_PATH = ""

    def __init__(self):
        self._memory_lock = threading.Lock()

    @abstractmethod
    def write_to_memory(self,
                        content: Any) -> None:
        pass

    @abstractmethod
    def read_from_memory(self) -> str:
        pass


class CustomOS(IOS):
    MEMORY_PATH = os.path.join(os.path.dirname(__file__), "result.txt")

    def __init__(self) -> None:
        super().__init__()

        if not os.path.exists(CustomOS.MEMORY_PATH):
            with open(CustomOS.MEMORY_PATH, "w"):
                pass

    def write_to_memory(self,
                        content: Any) -> None:
        with (self._memory_lock,
              open(CustomOS.MEMORY_PATH, "w") as f):
            f.write(str(content))

    def read_from_memory(self) -> str:
        with (self._memory_lock,
              open(CustomOS.MEMORY_PATH, "r") as f):
            return f.read().strip()
