import io
import os
import subprocess

from contextlib import redirect_stdout


class CustomShell:
    SSD_FILEPATH = os.path.join(os.path.dirname(__file__), "../ssd/ssd.py")

    def __init__(self,
                 src_path: str = os.path.dirname(__file__) + "/../ssd/result.txt") -> None:
        self.__src_path = src_path

    def session(self) -> None:
        while True:
            args = input().split()
            if len(args) == 0: continue

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
        try:
            subprocess.run(["python", self.SSD_FILEPATH, "W", str(lba), val],
                           shell=True, check=True, text=True, timeout=15, capture_output=True)
        except subprocess.CalledProcessError:
            raise

    def read(self,
             lba: int) -> None:
        try:
            subprocess.run(["python", self.SSD_FILEPATH, "R", str(lba)],
                           shell=True, check=True, text=True, timeout=15, capture_output=True)
        except subprocess.CalledProcessError:
            raise

        with open(self.__src_path, "r") as f:
            print(f"{[int(lba)]} - {f.readline()}")

    def exit(self) -> None:
        print("Exiting session.")

    def help(self) -> None:
        print("write(lba, val) - writes a val on lba")
        print("read(lba)       - reads the val written on lba")
        print("exit()          - exits program")
        print("help()          - prints manual to stdout")
        print("fullwrite(val)  - writes val to all lbas ranging from 0 to 99")
        print("fullread()      - reads all vals written on each lba ranging from 0 to 99 and prints to stdout")
        print("testapp1()      - runs testapp1, which performs fullwrite and fullread")
        print("testapp2()      - runs testapp2, which performs write aging followed by read compare")

    def fullwrite(self,
                  val: str) -> None:
        for lba in range(0, 100):
            self.write(lba, val)

    def fullread(self) -> None:
        for lba in range(0, 100):
            self.read(lba)

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
