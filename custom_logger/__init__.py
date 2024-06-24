import re
import glob
import inspect
import os.path
import threading
from datetime import datetime

from util import Singleton


class Logger(metaclass=Singleton):
    LOG_LEVEL_MIN = 0
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    LOG_LEVEL_MAX = 4

    def __init__(self) -> None:
        self.__log_lock = threading.Lock()
        self.__max_filesize = 10 * 1024

        self.__log_level_lock = threading.Lock()
        self.__log_level = Logger.DEBUG

        self.__root = os.path.dirname(__file__)
        self.__log_file = os.path.join(self.__root, "latest.log")
        self.__prepare_log_file()

    def set_log_level(self,
                      log_level: int) -> None:
        assert Logger.LOG_LEVEL_MIN <= log_level <= Logger.LOG_LEVEL_MAX

        with self.__log_level_lock:
            self.__log_level = log_level

    def debug(self,
              msg: str) -> None:
        if self.__log_level > Logger.DEBUG:
            return

        self.__log("DBG", msg)

    def info(self,
             msg: str) -> None:
        if self.__log_level > Logger.INFO:
            return

        self.__log("INFO", msg)

    def warn(self,
             msg: str) -> None:
        if self.__log_level > Logger.WARNING:
            return

        self.__log("WARN", msg)

    def error(self,
              msg: str) -> None:
        if self.__log_level > Logger.ERROR:
            return

        self.__log("ERR", msg)

    def critical(self,
                 msg: str) -> None:
        if self.__log_level > Logger.CRITICAL:
            return

        self.__log("CRIT", msg)

    def __log(self,
              log_level_str: str,
              msg: str) -> None:
        self.__flush_log_if_exceeds_maximum_size()

        frame = inspect.currentframe().f_back.f_back
        caller_function_name = frame.f_code.co_name

        with (self.__log_lock,
              open(self.__log_file, "a") as f):
            timestamp = datetime.now().strftime("%y.%m.%d %H:%M:%S")

            caller_function_name += "()"
            f.write(f"[{timestamp}][{log_level_str:<4}] {caller_function_name:<30} {msg}\n")

    def __flush_log_if_exceeds_maximum_size(self) -> None:
        with self.__log_lock:
            if os.path.getsize(self.__log_file) < self.__max_filesize:
                return

            self.__zip_old_log_files()

            timestamp = datetime.now().strftime("%y%m%d_%Hh_%Mm_%S.%fs")
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


LOGGER = Logger()
LOGGER.set_log_level(LOGGER.INFO)
