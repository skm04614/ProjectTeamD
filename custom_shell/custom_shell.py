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
                    if not method(*args[1:]):
                        break
                except TypeError:
                    print(f"INVALID SET OF PARAMETERS PROVIDED FOR '{method.__name__}'.")
                    print("Use 'help' to see the manual.")
            else:
                print("INVALID COMMAND")

    def write(self,
              lba: int,
              val: str) -> bool:
        result = subprocess.run(["python", self.SSD_FILEPATH, "W", str(lba), val],
                                capture_output=True,
                                text=True)
        if result.returncode:
            print(result.stderr)
            return True

        return True

    def read(self,
             lba: int) -> bool:
        result = subprocess.run(["python", self.SSD_FILEPATH, "R", str(lba)],
                                capture_output=True,
                                text=True)
        if result.returncode:
            print(result.stderr)
            return True

        with open(self.__src_path, "r") as f:
            print(f"{[int(lba)]} - {f.readline()}")

        return True

    def exit(self) -> bool:
        print("Exiting session.")

        return False

    def help(self) -> bool:
        print("write(lba, val) - writes a val on lba")
        print("read(lba)       - reads the val written on lba")
        print("exit()          - exits program")
        print("help()          - prints manual to stdout")
        print("full_write(val) - writes val to all lbas ranging from 0 to 99")
        print("full_read()     - reads all vals written on each lba ranging from 0 to 99 and prints to stdout")
        print("testapp1()      - runs testapp1, which performs fullwrite and fullread")

        return True

    def full_write(self,
                   val: str) -> bool:
        for lba in range(0, 100):
            self.write(lba, val)

        return True

    def full_read(self) -> bool:
        for lba in range(0, 100):
            self.read(lba)

        return True

    def testapp1(self) -> bool:
        test_value = "0x1234ABCD"
        expected_result = "\n".join([f"[{lba}] - {test_value}" for lba in range(0, 100)])
        self.full_write(test_value)
        with io.StringIO() as buf, redirect_stdout(buf):
            self.full_read()
            result = buf.getvalue().strip()
        print(result)
        print(f"TestApp1 was {'successful' if expected_result == result else 'failed'}!")

        return True


if __name__ == "__main__":
    cshell = CustomShell()
    cshell.session()
