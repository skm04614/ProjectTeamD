import io
import os
from unittest import TestCase, skip
from unittest.mock import Mock, patch
from contextlib import redirect_stdout

from custom_shell.custom_shell import CustomShell


def _lba_to_sample_val(lba: int) -> int:
    return lba << 4


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
                self.__cshell.write(lba, val)
                with io.StringIO() as buf, redirect_stdout(buf):
                    self.__cshell.read(lba)
                    result = buf.getvalue().strip()

                    self.assertEqual(f"[{lba}] - {val}", result)

    @skip
    def test_exception_when_invalid_argument_for_write(self):
        test_arg = [[-1, 0x12345678], [101, 0x12345678], [10, 0x1234ABCDD], [10, 'abcd'], [None, 0x1234ABCD],
                    [10, None]]

        for lba, val in test_arg:
            with self.assertRaises(ValueError):
                self.__cshell.write(lba, val)

    @skip
    def test_exception_when_invalid_argument_for_read(self):
        test_lbas = [-1, 101, '10', '', ' ', None]
        for lba in test_lbas:
            with self.assertRaises(ValueError):
                self.__cshell.read(lba)

    def test_exit(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            exit_code = self.__cshell.exit()
            result = buf.getvalue().strip()
            self.assertEqual("Exiting session.", result)
            self.assertFalse(exit_code)

    def test_help(self):
        expected = ("write(lba, val) - writes a val on lba",
                    "read(lba)       - reads the val written on lba",
                    "exit()          - exits program",
                    "help()          - prints manual to stdout",
                    "full_write(val) - writes val to all lbas ranging from 0 to 99",
                    "full_read()     - reads all vals written on each lba ranging from 0 to 99 and prints to stdout")
        expected = '\n'.join(expected)

        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.help()
            result = buf.getvalue().strip()
            self.assertEqual(expected, result)

    def test_full_write_followed_by_full_read(self):
        val = "0x1A2B3C4D"

        self.__cshell.full_write(val)
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.full_read()
            result = buf.getvalue().strip()
            expected = '\n'.join(f"[{lba}] - {val}" for lba in range(0, 100))

            self.assertEqual(expected, result)

    @patch.object(CustomShell, "read", side_effect=_print_lba_to_sample_val)
    def test_patched_full_read(self, mk_cshell):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.full_read()
            result = buf.getvalue().strip()
            expected = '\n'.join(str(_lba_to_sample_val(lba)) for lba in range(0, 100))
            self.assertEqual(expected, result)
