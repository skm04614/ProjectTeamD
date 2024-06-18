import io

from contextlib import redirect_stdout
from unittest import TestCase, skip
from unittest.mock import Mock

from custom_shell.custom_shell import CustomShell


class TestCustomShell(TestCase):
    def test_write(self):
        pass

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
        pass

    def test_full_write(self):
        pass

    def test_full_read(self):
        pass
