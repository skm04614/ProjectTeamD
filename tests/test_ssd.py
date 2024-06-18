from unittest import TestCase, skip

from ssd.ssd import SSD


class TestSSD(TestCase):
    def setUp(self):
        self.ssd = SSD()

    def test_write(self):
        pass

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
        invalid_lbas = [-1, 100]

        for lba in invalid_lbas:
            with self.subTest(f'SSD read test with out of range LBA: {lba}'):
                try:
                    self.ssd.read(lba)
                    self.fail("ValueError should have been raised.")
                except ValueError as err:
                    self.assertEqual("LBA is out of range [0, 100).", err.args[0])

    @skip
    def test_read_with_none_integer_lba(self):
        invalid_lbas = [' ', '', [], {}]

        for lba in invalid_lbas:
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
