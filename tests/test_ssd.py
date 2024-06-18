from unittest import TestCase

from ssd.ssd import SSD


class TestSSD(TestCase):
    def test_write(self):
        pass

    def test_read(self):
        sut = SSD()
        sut.get_data()[33] = 0x76543210

        sut.read(33)

        with open(sut.result_path, "r") as f:
            self.assertEqual(0x76543210, int(f.read(), 16))
