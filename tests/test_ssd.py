from unittest import TestCase, skip

from ssd.ssd import SSD


class TestSSD(TestCase):
    def test_write(self):
        pass

    def test_read(self):
        lba = 33
        expected = 0x76543210

        # arrange
        sut = SSD()
        sut.data[lba] = expected

        # act
        sut.read(lba)

        # assert
        with open(sut.result_path, "r") as f:
            self.assertEqual(expected, int(f.read(), 16))

    @skip
    def test_read_with_invalid_lba(self):
        invalid_lbas = [-1, 100, ' ', '', None]
        sut = SSD()

        for lba in invalid_lbas:
            with self.subTest(f'SSD read test with invalid lba: {lba}'):
                with self.assertRaises(ValueError):
                    sut.read(lba)
