import io
import os
import subprocess

from unittest import TestCase, skip
from unittest.mock import patch
from contextlib import redirect_stdout
from custom_shell.cshell import CustomShell


def _lba_to_sample_val(lba: int) -> str:
    return f"0x{lba << 4:08X}"


def _print_lba_to_sample_val(lba: int) -> None:
    print(_lba_to_sample_val(lba))


class TestCustomShell(TestCase):
    def setUp(self):
        super().setUp()
        self.__cshell = CustomShell()
        self.__cshell.session()

    @skip
    @patch("builtins.input", side_effect=["exit"])
    def tearDown(self):
        pass


    @skip
    @patch("builtins.input", side_effect=["write 99 0x0x1A2B3C4D", "read 99"])
    def test_successful_write_followed_by_read(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            result = buf.getvalue().strip()
            self.assertEqual(f"[99] - 0x0x1A2B3C4D", result)

    @skip
    def test_out_of_range_lba_read(self):
        invalid_lbas = (-1, 100, 170)
        for lba in invalid_lbas:
            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.read(lba)

    @skip
    def test_out_of_range_lba_write(self):
        invalid_lbas = (-1, 100, 170)
        for lba in invalid_lbas:
            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.write(lba, "0x12345678")

    @skip
    def test_out_of_range_val_write(self):
        invalid_vals = ("-0x1234", "0x1111222233", "0x000000001")
        for val in invalid_vals:
            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.write(0, val)

    @skip
    def test_exit(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            exit_code = self.__cshell.exit()
            result = buf.getvalue().strip()
            self.assertEqual("Exiting session.", result)
            self.assertFalse(exit_code)

    @skip
    def test_help(self):
        with open(os.path.dirname(__file__) + "/../custom_shell/help.txt", "r") as file:
            expected = file.read()

        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.help()
            result = buf.getvalue().strip()
            self.assertEqual(expected, result)

    @skip
    def test_out_of_range_val_fullwrite(self):
        invalid_vals = ("-0x1234", "0x1111222233", "0x000000001")
        for val in invalid_vals:
            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.fullwrite(val)

    @skip
    def test_fullwrite_followed_by_fullread(self):
        val = "0x1A2B3C4D"

        self.__cshell.fullwrite(val)
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.fullread()
            result = buf.getvalue().strip()
            expected = "\n".join(f"[{lba}] - {val}" for lba in range(0, 100))

            self.assertEqual(expected, result)

    @skip
    def test_successful_testapp1(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.testapp1()
            result = buf.getvalue().strip()

        test_value = "0x1234ABCD"
        expected_result = "\n".join([f"[{lba}] - {test_value}" for lba in range(0, 100)])
        expected_result += "\nTestApp1 ran successfully!"

        self.assertEqual(expected_result, result)

    @skip
    def test_successful_testapp2(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.testapp2()
            result = buf.getvalue().strip()

        self.assertEqual("TestApp2 executed successfully.", result)

    @skip
    @patch("builtins.input", side_effect=["write 0 0x12345678", "read 0", "exit"])
    def test_session_write_read_exit(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("[0] - 0x12345678", result[0])
            self.assertEqual("Exiting session.", result[1])

    @skip
    @patch("builtins.input", side_effect=["invalid_command", "exit"])
    def test_session_invalid_command(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("INVALID COMMAND", result[0])
            self.assertEqual("Exiting session.", result[1])

    @skip
    @patch("builtins.input", side_effect=["write 0", "exit"])
    def test_session_invalid_parameters(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("INVALID SET OF PARAMETERS PROVIDED FOR 'write'.", result[0])
            self.assertEqual("Use 'help' to see the manual.", result[1])
            self.assertEqual("Exiting session.", result[2])
