import os
from unittest import TestCase, skip
from unittest.mock import patch

from custom_shell.custom_shell import CustomShell


class TestCustomShell(TestCase):
    def setUp(self):
        self.customShell = CustomShell()

    def get_hex_values(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        hex_values = []
        for line in lines:
            parts = line.strip().split(' ')
            hex_value = parts[-1]
            hex_values.append(hex_value)
        return hex_values

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
        invalid_value = 0x1234FFFF1
        with self.assertRaises(ValueError):
            self.customShell.full_write(invalid_value)

    @skip
    def test_full_write(self):
        valid_value = 0x1234FFFF
        nand_path = os.path.dirname(__file__) + "/../ssd/nand.txt"
        self.customShell.full_write(valid_value)

        hex_values = self.get_hex_values(nand_path)
        for index, line in enumerate(hex_values):
            with self.subTest(f'lba:{index} value:{line}'):
                self.assertEqual(valid_value, int(line))

    def test_full_read(self):
        pass
