from unittest import TestCase

from ssd.ssd import SSD


class TestSSD(TestCase):
    def test_write(self):
        pass

    def test_read(self):
        lba = 33
        expected = 0x76543210
        result_path = './result.txt'

        # arrange
        sut = SSD(result_path=result_path)
        sut.get_data()[lba] = expected

        # act
        sut.read(lba)

        # assert
        with open(result_path, "r") as f:
            self.assertEqual(expected, int(f.read(), 16))
