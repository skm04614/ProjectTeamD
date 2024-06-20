import io

from abc import ABC, abstractmethod
from contextlib import redirect_stdout

from custom_shell.cshell import CustomShell

class Scenario(ABC):
    @abstractmethod
    def execute(self):
        pass


class TESTAPP1(Scenario):
    def execute(self):
        test_value = "0x1234ABCD"
        expected_result = "\n".join([f"[{lba}] - {test_value}" for lba in range(0, 100)])
        CustomShell._invoke_command(CustomShell._command_factory(*["fullwrite", test_value]))
        with io.StringIO() as buf, redirect_stdout(buf):
            CustomShell._invoke_command(CustomShell._command_factory(*["fullread"]))
            result = buf.getvalue().strip()
        print(result)
        print(f"TestApp1 {'ran successfully' if expected_result == result else 'failed'}!")


class TESTAPP2(Scenario):
    def execute(self):
        lower_lba = 0
        upper_lba = 5

        val = "0xAAAABBBB"
        for _ in range(30):
            for lba in range(lower_lba, upper_lba + 1):
                CustomShell._invoke_command(CustomShell._command_factory(*["write", lba, val]))

        val = "0x12345678"
        for lba in range(lower_lba, upper_lba + 1):
            CustomShell._invoke_command(CustomShell._command_factory(*["write", lba, val]))

        for lba in range(lower_lba, upper_lba + 1):
            with io.StringIO() as buf, redirect_stdout(buf):
                CustomShell._invoke_command(CustomShell._command_factory(*["read", lba]))
                result = buf.getvalue().strip()
                expected = f"[{lba}] - {val}"
                if result != expected:
                    print(f"TestApp2 failed at LBA[{lba}]")
                    print(f"Expected={expected}")
                    print(f"Actual={result}")
                    return

        print(f"TestApp2 executed successfully.")


class TESTAPP3(Scenario):
    def execute(self):
        print("testapp3")


class TESTAPP4(Scenario):
    def execute(self):
        print("testapp4")