import re
import glob
import os.path
import threading
from datetime import datetime

from util import Singleton


class Logger(metaclass=Singleton):
    def __init__(self) -> None:
        self.__log_lock = threading.Lock()
        self.__max_filesize = 10 * 1024

        self.__root = os.path.dirname(__file__)
        self.__log_file = os.path.join(self.__root, "latest.log")
        self.__prepare_log_file()

    def log(self,
            caller_function_name: str,
            msg: str) -> None:
        self.__flush_log_if_exceeds_maximum_size()

        with (self.__log_lock,
              open(self.__log_file, "a") as f):
            timestamp = datetime.now().strftime("%y.%m.%d %H:%M:%S")

            caller_function_name += "()"
            f.write(f"[{timestamp}] {caller_function_name:<30} {msg}\n")

    def __flush_log_if_exceeds_maximum_size(self) -> None:
        with self.__log_lock:
            if os.path.getsize(self.__log_file) < self.__max_filesize:
                return

            self.__zip_old_log_files()

            timestamp = datetime.now().strftime("%y%m%d_%Hh_%Mm_%Ss")
            renamed_log_file = os.path.join(self.__root,
                                            f"until_{timestamp}.log")
            os.rename(self.__log_file, renamed_log_file)

    def __zip_old_log_files(self) -> None:
        for old_log_file in glob.glob(os.path.join(self.__root, "until_*.log")):
            zipped_file = re.sub(r"[.]log$", ".zip", old_log_file)
            os.rename(old_log_file, zipped_file)

    def __prepare_log_file(self) -> None:
        if not os.path.exists(self.__log_file):
            with open(self.__log_file, "w"):
                pass
