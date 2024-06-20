import io
import os
import subprocess

from contextlib import redirect_stdout

from custom_shell.commands import WriteCommand, ReadCommand, EraseCommand
from custom_shell.invoker import invoke_command



class CustomShell:
    def __init__(self) -> None:

        with open(os.path.dirname(__file__) + "/help.txt", "r") as file:
            self.__help_content = file.read()

    def session(self) -> None:
        while True:
            args = input().split()
            if not args:
                continue

            method = getattr(self, args[0], None)
            if callable(method):
                try:
                    method(*args[1:])
                    if method.__name__ == "exit":
                        return
                except TypeError:
                    print(f"INVALID SET OF PARAMETERS PROVIDED FOR '{method.__name__}'.")
                    print("Use 'help' to see the manual.")
                except subprocess.CalledProcessError as e:
                    print(e.stderr)
            else:
                print("INVALID COMMAND")

    def write(self,
              lba: int,
              val: str) -> None:
        invoke_command(WriteCommand(lba, val))

    def read(self,
             lba: int) -> None:
        invoke_command(ReadCommand(lba))

    def exit(self) -> None:
        print("Exiting session.")

    def help(self) -> None:
        print(self.__help_content)

    def fullwrite(self,
                  val: str) -> None:
        for lba in range(0, 100):
            self.write(lba, val)

    def fullread(self) -> None:
        for lba in range(0, 100):
            self.read(lba)

    def erase(self,
              lba: int,
              size: int) -> None:
        self.erase_range(lba, lba + size - 1)

    def erase_range(self,
                    start_lba: int,
                    end_lba: int) -> None:
        invoke_command(EraseCommand(start_lba, end_lba))

    def testapp1(self) -> None:
        test_value = "0x1234ABCD"
        expected_result = "\n".join([f"[{lba}] - {test_value}" for lba in range(0, 100)])
        self.fullwrite(test_value)
        with io.StringIO() as buf, redirect_stdout(buf):
            self.fullread()
            result = buf.getvalue().strip()
        print(result)
        print(f"TestApp1 {'ran successfully' if expected_result == result else 'failed'}!")

    def testapp2(self) -> None:
        lower_lba = 0
        upper_lba = 5

        val = "0xAAAABBBB"
        for _ in range(30):
            for lba in range(lower_lba, upper_lba + 1):
                self.write(lba, val)

        val = "0x12345678"
        for lba in range(lower_lba, upper_lba + 1):
            self.write(lba, val)

        for lba in range(lower_lba, upper_lba + 1):
            with io.StringIO() as buf, redirect_stdout(buf):
                self.read(lba)
                result = buf.getvalue().strip()
                expected = f"[{lba}] - {val}"
                if result != expected:
                    print(f"TestApp2 failed at LBA[{lba}]")
                    print(f"Expected={expected}")
                    print(f"Actual={result}")
                    return

        print(f"TestApp2 executed successfully.")


if __name__ == "__main__":
    cshell = CustomShell()
    cshell.session()
