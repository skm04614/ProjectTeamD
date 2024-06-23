import os
import re
import sys
import subprocess

import testing_suite
from custom_shell.command import *


class CustomShell:
    def session(self) -> None:
        while True:
            args = input("==================================================\n>> ").split()
            if not args:
                print("Use 'help' to see the manual.")
                continue

            operation = args[0]
            if operation == "exit":
                print("Exiting session.")
                return

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
        print("##########################  Runner Start  ##########################")
        try:
            if not os.path.isabs(test_scenario_path):
                test_scenario_path = os.path.join(os.path.dirname(__file__), test_scenario_path)

            if not os.path.exists(test_scenario_path):
                print(f"Path '{test_scenario_path}' does not exist.")
                return

            testable_scenarios = testing_suite.get_tests()

            with open(test_scenario_path, "r") as f:
                for scenario in (line.strip() for line in f):
                    trimmed_scenario = scenario[:46]
                    print(f"* {trimmed_scenario} {'-' * (50 - len(trimmed_scenario))} ",
                          end="",
                          flush=True)

                    if scenario not in testable_scenarios:
                        print(f"DOES NOT EXIST!!!")
                        return

                    print("Run...", end="", flush=True)
                    if not testable_scenarios[scenario]():
                        print("FAIL!")
                        return

                    print("Pass")
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

        raise ICommand.UnsupportedException(f"Requested operation, '{operation}', is not supported.")


if __name__ == "__main__":
    cshell = CustomShell()

    if len(sys.argv) > 1:
        cshell.run(sys.argv[1])
    else:
        cshell.session()
