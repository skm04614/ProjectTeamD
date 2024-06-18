from unittest import TestCase, skip
from unittest.mock import patch

from shell import Shell


class TestCustomShell(TestCase):
    def test_write(self):
        pass

    def test_read(self):
        pass

    def test_exit(self):
        pass

    def test_help(self):
        pass

    @skip
    def test_full_write_invalid_value(self):
        shell = Shell()
        invalid_value = 0x1234FFFF1
        with self.assertRaises(ValueError):
            shell.full_write(invalid_value)

    @skip
    def test_full_write(self):
        shell = Shell()
        valid_value = '0x1234FFFF'
        file_path = './nand.txt'
        shell.full_write(valid_value)

        with open(file_path, 'r') as file:
            lines = file.readlines()
        for index, line in enumerate(lines):
            with self.subTest(f'lba:{index} value:{line.strip()}'):
                self.assertEqual(valid_value, line.strip())

    def test_full_read(self):
        pass
