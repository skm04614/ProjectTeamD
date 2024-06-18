import os.path
from unittest import TestCase, skip
from unittest.mock import Mock

from custom_shell.custom_shell import CustomShell


class TestCustomShell(TestCase):
    def setUp(self):
        super().setUp()
        self.cshell = CustomShell()

    @skip
    def test_write(self):
        self.cshell.write(10, 0x1234ABCD)
        self.cshell.read(10)

        with open(os.path.dirname(__file__) + '\\..\\ssd\\result.txt', 'r') as f:
            ret = f.read().strip()

        self.assertEqual(0x1234ABCD, int(ret, 6))

    @skip
    def test_exception_when_invalid_argument_for_write(self):
        test_arg = [[-1, 0x12345678], [101, 0x12345678], [10, 0x1234ABCDD], [10, 'abcd'], [None, 0x1234ABCD],
                    [10, None]]

        for lba, val in test_arg:
            with self.assertRaises(ValueError):
                self.cshell.write(lba, val)

    def test_read(self):
        pass

    def test_exit(self):
        pass

    def test_help(self):
        pass

    def test_full_write(self):
        pass

    def test_full_read(self):
        pass
