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
        ssd = Mock()
        ssd_results = [f'0x{i:08X}' for i in range(100)]
        ssd.read.side_effect = ssd_results
        shell = Shell()
        self.assertEqual(ssd.call_count, 100)
        self.assertEqual(shell.full_read(), '\n'.join(ssd_results))
