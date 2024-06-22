import sys

import testing_suite
from custom_shell.command import *


class CustomShell:
    def session(self) -> None:
        while True:
            args = input("==================================================\n>> ").split()
            if not args:
                continue

            operation = args[0]
            if operation == "exit":
                print("Exiting session.")
                return

            # TODO: refactor out testapp1 and testapp2
            try:
                self.execute(*args)
            except ICommand.UnsupportedException:
                print("INVALID COMMAND")
            except (TypeError, IndexError):
                print(f"INVALID SET OF PARAMETERS PROVIDED FOR '{operation}'.")
                print("Use 'help' to see the manual.")
            except ValueError:
                print(f"'{operation}' IS CALLED WITH INVALID TYPED SET OF PARAMETERS.")
                print("Use 'help' to see the manual.")
            except subprocess.CalledProcessError as e:
                print(e.stderr)

    def execute(self,
                *args) -> None:
        CustomShell._invoke_command(CustomShell._command_factory(*args))

    @staticmethod
    def _invoke_command(command: ICommand) -> None:
        command.execute()

    @staticmethod
    def _command_factory(operation: str,
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


if __name__ == "__main__":
    cshell = CustomShell()

    if len(sys.argv) > 1:
        cshell.run(sys.argv[1])
    else:
        cshell.session()
