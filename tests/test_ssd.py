from unittest import TestCase, skip

from ssd.ssd import SSD


class TestSSD(TestCase):
    def setUp(self):
        super().setUp()
        self.ssd = SSD()

    @skip
    def test_exception_when_invalid_argument_for_write(self):
        test_arg = [[-1, 0x12345678], [101, 0x12345678], [10, 0x1234], [10, 0x1234ABCDD], [10, 'abcd']]

        for lba, val in test_arg:
            with self.assertRaises(ValueError):
                self.ssd.write(lba, val)

    @skip
    def test_success_write(self):
        self.ssd.write(10, 0x1234ABCD)
        with open('../ssd/result.txt', 'r') as f:
            ret = f.read()
        self.assertEqual(int(ret, 16), 0x1234ABCD)

    def test_read(self):
        pass
