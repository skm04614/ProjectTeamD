import io
import os
import subprocess

from unittest import TestCase
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

    def test_successful_write_followed_by_read(self):
        valid_lbas = (0, 35, 99)
        valid_vals = ("0x00000000", "0xFFFFFFFF", "0x1A2B3C4D")
        for lba in valid_lbas:
            for val in valid_vals:
                self.__cshell.execute("write", lba, val)
                with io.StringIO() as buf, redirect_stdout(buf):
                    self.__cshell.execute("read", lba)
                    result = buf.getvalue().strip()
                    self.assertEqual(f"[{lba}] - {val}", result)

    def test_out_of_range_lba_read(self):
        invalid_lbas = (-1, 100, 170)
        for lba in invalid_lbas:
            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.execute("read", lba)

    def test_out_of_range_lba_write(self):
        invalid_lbas = (-1, 100, 170)
        for lba in invalid_lbas:
            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.execute("write", lba, "0x12345678")

    def test_out_of_range_val_write(self):
        invalid_vals = ("-0x1234", "0x1111222233", "0x000000001")
        for val in invalid_vals:
            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.execute("write", 0, val)

    def test_help(self):
        with open(os.path.join(os.path.dirname(__file__),
                               "../custom_shell/help.txt"), "r") as file:
            expected = file.read()

        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.execute("help")
            result = buf.getvalue().strip()
            self.assertEqual(expected, result)

    def test_out_of_range_val_fullwrite(self):
        invalid_vals = ("-0x1234", "0x1111222233", "0x000000001")
        for val in invalid_vals:
            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.execute("fullwrite", val)

    def test_fullwrite_followed_by_fullread(self):
        val = "0x1A2B3C4D"

        self.__cshell.execute("fullwrite", val)
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.execute("fullread")
            result = buf.getvalue().strip()
            expected = "\n".join(f"[{lba}] - {val}" for lba in range(0, 100))

            self.assertEqual(expected, result)

    def test_successful_testapp1(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.testapp1()
            result = buf.getvalue().strip()

        test_value = "0x1234ABCD"
        expected_result = "\n".join([f"[{lba}] - {test_value}" for lba in range(0, 100)])
        expected_result += "\nTestApp1 ran successfully!"

        self.assertEqual(expected_result, result)

    def test_successful_testapp2(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.testapp2()
            result = buf.getvalue().strip()

        self.assertEqual("TestApp2 executed successfully.", result)

    @patch("builtins.input", side_effect=["write 0 0x12345678", "read 0", "exit"])
    def test_session_write_read_exit(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("[0] - 0x12345678", result[0])
            self.assertEqual("Exiting session.", result[1])

    @patch("builtins.input", side_effect=["invalid_command", "exit"])
    def test_session_invalid_command(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("INVALID COMMAND", result[0])
            self.assertEqual("Exiting session.", result[1])

    @patch("builtins.input", side_effect=["write 0", "exit"])
    def test_session_invalid_parameters(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("INVALID SET OF PARAMETERS PROVIDED FOR 'write'.", result[0])
            self.assertEqual("Use 'help' to see the manual.", result[1])
            self.assertEqual("Exiting session.", result[2])

    @patch("builtins.input", side_effect=["write 1 0x123AFE18", "erase 1 1", "read 1", "exit"])
    def test_erase_size_just_one_lba(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("[1] - 0x00000000", result[0])
