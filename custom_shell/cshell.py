import io
import sys

from contextlib import redirect_stdout
from custom_shell.commands import *


class CustomShell:
    def session(self) -> None:
        while True:
            args = input().split()
            if not args:
                continue

            operation = args[0]
            if operation == "exit":
                print("Exiting session.")
                return

            # TODO: refactor out testapp1 and testapp2
            if operation == "testapp1":
                self.testapp1()
            elif operation == "testapp2":
                self.testapp2()
            else:
                try:
                    CustomShell.invoke_command(CustomShell.command_factory(*args))
                except InvalidCommandException:
                    print("INVALID COMMAND")
                except TypeError:
                    print(f"INVALID SET OF PARAMETERS PROVIDED FOR '{operation}'.")
                    print("Use 'help' to see the manual.")
                except subprocess.CalledProcessError as e:
                    print(e.stderr)

    @staticmethod
    def invoke_command(command: ICommand) -> None:
        command.execute()

    @staticmethod
    def command_factory(operation: str,
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

        raise InvalidCommandException(f"Requested operation, '{operation}', is not supported.")

    def testapp1(self) -> bool:
        test_value = "0x1234ABCD"
        expected_result = "\n".join([f"[{lba}] - {test_value}" for lba in range(0, 100)])

        CustomShell.invoke_command(CustomShell.command_factory("fullwrite", test_value))
        with io.StringIO() as buf, redirect_stdout(buf):
            CustomShell.invoke_command(CustomShell.command_factory("fullread"))
            result = buf.getvalue().strip()
        print(result)
        print(f"TestApp1 {'ran successfully' if expected_result == result else 'failed'}!")

        return expected_result == result

    def testapp2(self) -> bool:
        lower_lba = 0
        upper_lba = 5

        val = "0xAAAABBBB"
        for _ in range(30):
            for lba in range(lower_lba, upper_lba + 1):
                CustomShell.invoke_command(CustomShell.command_factory("write", lba, val))

        val = "0x12345678"
        for lba in range(lower_lba, upper_lba + 1):
            CustomShell.invoke_command(CustomShell.command_factory("write", lba, val))

        for lba in range(lower_lba, upper_lba + 1):
            with io.StringIO() as buf, redirect_stdout(buf):
                CustomShell.invoke_command(CustomShell.command_factory("read", lba))

                result = buf.getvalue().strip()
                expected = f"[{lba}] - {val}"
                if result != expected:
                    print(f"TestApp2 failed at LBA[{lba}]")
                    print(f"Expected={expected}")
                    print(f"Actual={result}")
                    return False

        print(f"TestApp2 executed successfully.")
        return True

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
