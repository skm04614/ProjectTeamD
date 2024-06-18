from unittest import TestCase

from ssd.ssd import SSD


class TestSSD(TestCase):
    def setUp(self):
        super().setUp()
        self.ssd = SSD()

    def assert_invalid_argument_for_write(self, lba, val):
        try:
            self.ssd.write(lba, val)
            self.fail()
        except TypeError:
            pass

    def test_exception_when_invalid_argument_for_write(self):
        self.assert_invalid_argument_for_write(-1, 0x12345678)
        self.assert_invalid_argument_for_write(101, 0x12345678)
        self.assert_invalid_argument_for_write(10, 0x1234)
        self.assert_invalid_argument_for_write(10, 0x1234ABCDD)
        self.assert_invalid_argument_for_write(10, 'abcd')

    def test_success_write(self):
        self.ssd.write(10, 0x1234ABCD)
        self.assertEqual(0x1234ABCD, self.ssd.read(10))

    def test_read(self):
        pass
