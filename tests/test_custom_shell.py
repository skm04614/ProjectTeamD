from unittest import TestCase
from unittest.mock import Mock

from custom_shell.custom_shell import CustomShell


class TestCustomShell(TestCase):
    def test_write(self):
        pass

    def test_read(self):
        ssd = Mock()
        ssd.read.return_value = "0xAABBCCDD"
        self.assertEqual(CustomShell().read(0), "0xAABBCCDD")

    def test_exit(self):
        pass

    def test_help(self):
        pass

    def test_full_write(self):
        pass

    def test_full_read(self):
        pass
