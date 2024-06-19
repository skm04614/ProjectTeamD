import io
from unittest import TestCase
from unittest.mock import patch
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

    def test_out_of_range_lba_read(self):
        invalid_lbas = (-1, 100, 170)
        for lba in invalid_lbas:
            with io.StringIO() as buf, redirect_stdout(buf):
                self.__cshell.read(lba)
                result = buf.getvalue().strip()

                self.assertIn("ValueError", result)

    def test_out_of_range_lba_write(self):
        invalid_lbas = (-1, 100, 170)
        for lba in invalid_lbas:
            with io.StringIO() as buf, redirect_stdout(buf):
                self.__cshell.write(lba, "0x12345678")
                result = buf.getvalue().strip()

                self.assertIn("ValueError", result)

    def test_out_of_range_val_write(self):
        invalid_vals = ("-0x1234", "0x1111222233", "0x000000001")
        for val in invalid_vals:
            with io.StringIO() as buf, redirect_stdout(buf):
                self.__cshell.write(0, val)
                result = buf.getvalue().strip()

                self.assertIn("ValueError", result)

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
                    "full_read()     - reads all vals written on each lba ranging from 0 to 99 and prints to stdout",
                    "testapp1()      - runs testapp1, which performs fullwrite and fullread")
        expected = '\n'.join(expected)

        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.help()
            result = buf.getvalue().strip()
            self.assertEqual(expected, result)

    def test_out_of_range_val_full_write(self):
        invalid_vals = ("-0x1234", "0x1111222233", "0x000000001")
        for val in invalid_vals:
            with io.StringIO() as buf, redirect_stdout(buf):
                self.__cshell.full_write(val)
                result = buf.getvalue().strip()

                self.assertIn("ValueError", result)

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
