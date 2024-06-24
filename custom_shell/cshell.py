import os
import re
import sys
import subprocess

import testing_suite
from custom_shell.command import *
from custom_logger import LOGGER


class CustomShell:
    def session(self) -> None:
        LOGGER.info("opened a new session.")
        while True:
            user_input = input("====================================================================\n>> ").strip()
            if not user_input:
                print("Use 'help' to see the manual.")
                continue

            if user_input == "exit":
                print("Exiting session.")
                return

            if user_input == "list_tc":
                print(*(tc for tc in testing_suite.get_tests()), sep="\n")
                continue

            args = user_input.split()
            if args[0] == "run":
                for scenario in args[1:]:
                    testing_suite.execute_scenario(scenario)
                continue

            try:
                self.execute(*args)
            except ICommand.UnsupportedException:
                print("INVALID COMMAND")
            except subprocess.CalledProcessError as e:
                error_pattern = re.compile(r"^\w+(Error|Exception).*", re.I)
                print(*(line for line in e.stderr.splitlines() if error_pattern.match(line)), sep="\n")
                print("Use 'help' to see the manual.")
            except Exception as e:
                print(f"{e.__class__.__name__}: {str(e)}")
                print("Use 'help' to see the manual.")

    def execute(self,
                *args) -> None:
        self._command_factory(*args).execute()

    def run(self,
            test_scenario_path: str) -> None:
        LOGGER.info("running test scenarios via runner.")

        print("##########################  Runner Start  ##########################")
        try:
            if not os.path.isabs(test_scenario_path):
                LOGGER.warn("scenario_path is provided as a relative path.")
                test_scenario_path = os.path.join(os.path.dirname(__file__), test_scenario_path)

            if not os.path.exists(test_scenario_path):
                LOGGER.critical(f"path '{test_scenario_path}' does not exist.")
                print(f"Path '{test_scenario_path}' does not exist.")
                return

            with open(test_scenario_path, "r") as f:
                for scenario in (line.strip() for line in f):
                    LOGGER.info(f"attempting to run {scenario}.")
                    if not testing_suite.execute_scenario(scenario):
                        LOGGER.critical(f"{scenario} failed... aborting runner.")
                        return
        finally:
            print("###########################  Runner End  ###########################")

    @classmethod
    def _command_factory(cls,
                         operation: str,
                         *args) -> ICommand:
        if operation == "read":
            return ReadCommand(*args)

        if operation == "write":
            return WriteCommand(*args)

        if operation == "fullwrite":
            return FullWriteCommand(*args)

        if operation == "fullread":
            return FullReadCommand(*args)

        if operation == "help":
            return HelpCommand(*args)

        if operation == "erase":
            return EraseSizeCommand(*args)

        if operation == "erase_range":
            return EraseRangeCommand(*args)

        if operation == "flush":
            return FlushCommand(*args)

        LOGGER.critical(f"The shell does not support '{operation}' command.")
        raise ICommand.UnsupportedException(f"Requested operation, '{operation}', is not supported.")


if __name__ == "__main__":
    cshell = CustomShell()

    if len(sys.argv) > 1:
        cshell.run(sys.argv[1])
    else:
        cshell.session()
