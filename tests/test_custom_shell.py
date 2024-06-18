import os.path
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
        self.cshell = CustomShell()
        self.__cshell = CustomShell()


    def get_hex_values(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        hex_values = []
        for line in lines:
            parts = line.strip().split(' ')
            hex_value = parts[-1]
            hex_values.append(hex_value)
        return hex_values


    @skip
    def test_write(self):
        self.cshell.write(10, 0x1234ABCD)
        self.cshell.read(10)

        with open(os.path.dirname(__file__) + '/../ssd/result.txt', 'r') as f:
            ret = f.read().strip()

        self.assertEqual(0x1234ABCD, int(ret, 16))

    @skip
    def test_exception_when_invalid_argument_for_write(self):
        test_arg = [[-1, 0x12345678], [101, 0x12345678], [10, 0x1234ABCDD], [10, 'abcd'], [None, 0x1234ABCD],
                    [10, None]]

        for lba, val in test_arg:
            with self.assertRaises(ValueError):
                self.cshell.write(lba, val)

    @skip
    def test_read(self):
        ssd = Mock()
        test_tables = {0: "0x00000000", 50: "0xAABBCCDD", 99: "0xAABBCCD0"}
        for lba, data in test_tables.items():
            with (self.subTest(f"lba: {lba}, ssd data read test!"),
                  io.StringIO() as buf, redirect_stdout(buf)):
                ssd.read.return_value = data
                CustomShell().read(lba)
                self.assertEqual(buf.getvalue().strip(), data)

    @skip
    def test_exception_when_invalid_argument_for_read(self):
        test_lbas = [-1, 101, '10', '', ' ', None]
        for lba in test_lbas:
            with self.assertRaises(ValueError):
                CustomShell().read(lba)

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

    @skip
    def test_full_write_invalid_value(self):
        invalid_value = 0x1234FFFFF
        with self.assertRaises(ValueError):
            self.__cshell.full_write(invalid_value)

    @skip
    def test_full_write(self):
        valid_value = 0x1234FFFF
        nand_path = os.path.dirname(__file__) + "/../ssd/nand.txt"
        self.__cshell.full_write(valid_value)

        hex_values = self.get_hex_values(nand_path)
        for index, line in enumerate(hex_values):
            with self.subTest(f'lba:{index} value:{line}'):
                formatted_value = hex(valid_value).upper().replace('0X', '0x')
                self.assertEqual(formatted_value, line)

    @patch.object(CustomShell, "read", side_effect=_print_lba_to_sample_val)
    def test_full_read(self, mk_cshell):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.__cshell.full_read()
            result = buf.getvalue().strip()
            expected = '\n'.join(str(_lba_to_sample_val(lba)) for lba in range(0, 100))
            self.assertEqual(expected, result)
