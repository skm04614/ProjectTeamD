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
        self.ssd._prepare_nand_data()
        self.assertEqual(self.ssd._data[10], 0x1234ABCD)

    @skip
    def test_read(self):
        lba = 33
        expected = 0x76543210

        # arrange
        self.ssd._data[lba] = expected

        # act
        self.ssd.read(lba)

        # assert
        with open(self.ssd.result_path, "r") as f:
            self.assertEqual(expected, int(f.read(), 16))

    @skip
    def test_read_with_out_of_range_lba(self):
        out_of_range_lbas = [-1, 100]

        for lba in out_of_range_lbas:
            with self.subTest(f'SSD read test with out of range LBA: {lba}'):
                try:
                    self.ssd.read(lba)
                    self.fail("ValueError should have been raised.")
                except ValueError as err:
                    self.assertEqual("LBA is out of range [0, 100).", err.args[0])

    @skip
    def test_read_with_none_integer_lba(self):
        none_integer_lbas = [' ', '', [], {}]

        for lba in none_integer_lbas:
            with self.subTest(f'SSD read test with none integer LBA: {lba}'):
                try:
                    self.ssd.read(lba)
                    self.fail("TypeError should have been raised.")
                except TypeError as err:
                    self.assertEqual("LBA must be an integer.", err.args[0])

    @skip
    def test_read_with_none_lba(self):
        try:
            self.ssd.read(None)
            self.fail("ValueError should have been raised.")
        except ValueError as err:
            self.assertEqual("LBA is required.", err.args[0])
