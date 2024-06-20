import io
import sys

from contextlib import redirect_stdout
from custom_shell.commands import *


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

            try:
                self.execute(*args)
            except ICommand.UnsupportedException:
                print("INVALID COMMAND")
            except (TypeError, IndexError):
                print(f"INVALID SET OF PARAMETERS PROVIDED FOR '{operation}'.")
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

        return ScenarioCommand(operation, *args)

    def runner(self,
               scenario_path: str) -> None:
        if not os.path.exists(scenario_path):
            print("Scenario does not exist.")
            return

        print("--------------------Runner Start--------------------")
        testable_scenarios = ('testapp1', 'testapp2')
        with open(scenario_path, "r") as f:
            for line in f:
                scenario = line.strip()
                print(f"{scenario:<20} --- Run...", end="", flush=True)

                method = getattr(self, scenario, None)
                if scenario in testable_scenarios and callable(method):
                    try:
                        with io.StringIO() as buf, redirect_stdout(buf):
                            result = method()

                        if not result:
                            print("Fail!")
                            break
                        print("Pass")
                    except subprocess.CalledProcessError:
                        print("Fail!")
                        break
                else:
                    print("INVALID SCENARIO")
                    break
        print("---------------------Runner End---------------------")


if __name__ == "__main__":
    cshell = CustomShell()

    if len(sys.argv) > 1:
        cshell.runner(sys.argv[1])
    else:
        cshell.session()
