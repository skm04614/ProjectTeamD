from unittest import TestCase, skip

from ssd.ssd import SSD


class TestSSD(TestCase):
    def setUp(self):
        super().setUp()
        self.ssd = SSD()

    def test_exception_when_invalid_arg_for_write(self):
        test_arg = [[-1, 0x12345678], [101, 0x12345678], [10, 0x1234], [10, 0x1234ABCDD], [10, 'abcd']]

        for lba, val in test_arg:
            with self.assertRaises(Exception):
                self.ssd.write(lba, val)

    def test_success_write(self):
        self.ssd.write(10, 0x1234ABCD)
        self.ssd._prepare_nand_data()
        self.assertEqual(self.ssd._data[10], 0x1234ABCD)

    @skip
    def test_read(self):
        lba = 33
        expected = 0x76543210

        # arrange
        self.ssd.data[lba] = expected

        # act
        self.ssd.read(lba)

        # assert
        with open(self.ssd.result_path, "r") as f:
            self.assertEqual(expected, int(f.read(), 16))

    @skip
    def test_read_with_invalid_lba(self):
        invalid_lbas = [-1, 100, ' ', '', None]

        for lba in invalid_lbas:
            with self.subTest(f'SSD read test with invalid lba: {lba}'):
                with self.assertRaises(ValueError):
                    self.ssd.read(lba)
