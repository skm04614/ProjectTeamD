import io
from unittest import TestCase, skip
from unittest.mock import patch
from contextlib import redirect_stdout

from custom_shell.custom_shell import CustomShell


def _lba_to_sample_val(lba: int) -> int:
    return lba << 4


def _print_lba_to_sample_val(lba: int) -> None:
    print(_lba_to_sample_val(lba))


class TestCustomShell(TestCase):
    def setUp(self):
        self.__cshell = CustomShell()

    def test_write(self):
        pass

    def test_read(self):
        pass

    def test_exit(self):
        pass

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

    def test_full_write(self):
        pass

    @skip
    @patch.object(CustomShell, "read", side_effect=_print_lba_to_sample_val)
    def test_full_read(self, mk_cshell):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.full_read()
            result = ', '.join(buf.getvalue().strip())
            expected = ', '.join(str(_lba_to_sample_val(lba)) for lba in range(0, 100))
            self.assertEqual(expected, result)
