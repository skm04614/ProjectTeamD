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
            with self.subTest(f"lba: {lba}, ssd data read test!"):
                ssd.read.return_value = data
                self.assertEqual(CustomShell().read(lba), data)

    def test_exit(self):
        pass

    def test_help(self):
        pass

    def test_full_write(self):
        pass

    def test_full_read(self):
        pass
