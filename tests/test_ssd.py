from unittest import TestCase

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
