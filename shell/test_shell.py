from unittest import TestCase
from unittest.mock import Mock

from shell_tester import ShellTester

class TestShell(TestCase):
    def test_write(self):
        pass

    def test_read(self):
        ssd = Mock()
        ssd.read.return_value = "0xAABBCCDD"
        self.assertEqual(ShellTester().read(0), "0xAABBCCDD")

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
        self.assertEqual(ShellTester().full_read(), '\n'.join(ssd_results))
