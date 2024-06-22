import io
import os
import subprocess
import numpy as np
from unittest import TestCase
from unittest.mock import patch
from contextlib import redirect_stdout

from custom_shell.cshell import CustomShell
from custom_ssd.cssd import SSD


def _lba_to_sample_val(lba: int) -> str:
    return f"0x{lba << 4:08X}"


def _print_lba_to_sample_val(lba: int) -> None:
    print(_lba_to_sample_val(lba))


class TestCustomShell(TestCase):
    def setUp(self):
        super().setUp()
        self.__cshell = CustomShell()

        self._valid_lbas = tuple(int(lba) for lba in np.linspace(SSD.LBA_LOWER_BOUND,
                                                                 SSD.LBA_UPPER_BOUND,
                                                                 7))

        self._valid_vals = ("0x00000000", "0x12345678", "0x33334444", "0x98765432",
                            "0xA1B2C3D4", "0xAFBECDAF", "0xFFFFFFFF")

        self._invalid_lbas = (-100, -1, 100, 150)
        self._wrong_typed_lbas = ([], None, "0", "1b", "a1")
        self._invalid_vals = ("0x0", "0x1234", "FFFF0000", "0x100000000", "-0x12345678")
        self._wrong_typed_vals = ([], None, 0xFFFFFFFF, 0x0)

    def test_successful_write_followed_by_read(self):
        for lba in self._valid_lbas:
            for val in self._valid_vals:
                self.__cshell.execute("write", lba, val)
                with io.StringIO() as buf, redirect_stdout(buf):
                    self.__cshell.execute("read", lba)
                    self.assertEqual(f"[{lba}] - {val}", buf.getvalue().strip())

    def test_invalid_lba_read_write(self):
        for lba in self._invalid_lbas:
            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.execute("read", lba)

            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.execute("write", lba, self._valid_vals[0])

    def test_invalid_val_write(self):
        for val in self._invalid_vals:
            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.execute("write", self._valid_lbas[0], val)

    def test_help(self):
        with open(os.path.join(os.path.dirname(__file__),
                               "../custom_shell/manual.txt"), "r") as file:
            expected = file.read()

        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.execute("help")
            self.assertEqual(expected, buf.getvalue().strip())

    def test_invalid_val_fullwrite(self):
        for val in self._invalid_vals:
            with self.assertRaises(subprocess.CalledProcessError):
                self.__cshell.execute("fullwrite", val)

    def test_fullwrite_followed_by_fullread(self):
        val = self._valid_vals[3]

        self.__cshell.execute("fullwrite", val)
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.execute("fullread")
            expected = "\n".join(f"[{lba}] - {val}" for lba in range(0, 100))

            self.assertEqual(expected, buf.getvalue().strip())

    @patch("builtins.input",
           side_effect=["write 0 0x12345678",
                        "read 0",
                        "exit"])
    def test_session_write_read_exit(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("[0] - 0x12345678", result[0])
            self.assertEqual("Exiting session.", result[1])

    @patch("builtins.input",
           side_effect=["invalid_command",
                        "exit"])
    def test_session_invalid_command(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("INVALID COMMAND", result[0])
            self.assertEqual("Exiting session.", result[1])

    @patch("builtins.input",
           side_effect=["write 0",
                        "exit"])
    def test_session_invalid_parameters(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("INVALID SET OF PARAMETERS PROVIDED FOR 'write'.", result[0])
            self.assertEqual("Use 'help' to see the manual.", result[1])
            self.assertEqual("Exiting session.", result[2])

    @patch("builtins.input",
           side_effect=["write 1 0x123AFE18",
                        "write 2 0x123AFE18",
                        "write 3 0x123AFE18",
                        "erase 2 1",
                        "read 1",
                        "read 2",
                        "read 3",
                        "exit"])
    def test_erase_size_just_one_lba(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("[1] - 0x123AFE18", result[0])
            self.assertEqual("[2] - 0x00000000", result[1])
            self.assertEqual("[3] - 0x123AFE18", result[2])

    @patch("builtins.input",
           side_effect=["fullwrite 0x123AFE18",
                        "erase_range 94 99",
                        "fullread",
                        "exit"])
    def test_successful_erase_range(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.session()
            result = buf.getvalue().strip().split("\n")
            self.assertEqual("[93] - 0x123AFE18", result[93])
            for idx in range(94, 99):
                self.assertEqual(f"[{idx}] - 0x00000000", result[idx])
            self.assertEqual("[99] - 0x123AFE18", result[99])
