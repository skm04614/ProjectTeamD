from unittest import TestCase, skip
from unittest.mock import Mock

from custom_shell.custom_shell import CustomShell


class TestCustomShell(TestCase):
    def setUp(self):
        super().setUp()

    def test_write_mock(self):
        mk = Mock()
        mk.write(10, 0x12345678)

        mk.write.assert_called_once_with(10, 0x12345678)

    @skip
    def test_exception_when_invalid_argument_for_write(self):
        cshell = CustomShell()

        test_arg = [[-1, 0x12345678], [101, 0x12345678], [10, 0x1234], [10, 0x1234ABCDD], [10, 'abcd'], [None, 0x1234ABCD], [10, None]]

        for lba, val in test_arg:
            with self.assertRaises(ValueError):
                cshell.write(lba, val)

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
