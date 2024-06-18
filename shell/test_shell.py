from unittest import TestCase
from unittest.mock import Mock

from shell import Shell

class TestShell(TestCase):
    def test_write(self):
        pass

    def test_read(self):
        ssd = Mock()
        ssd.read.return_value = "0xAABBCCDD"
        shell = Shell()
        self.assertEqual(shell.read(), "0xAABBCCDD")

    def test_exit(self):
        pass

    def test_help(self):
        pass

    def test_full_write(self):
        pass

    def test_full_read(self):
        pass
