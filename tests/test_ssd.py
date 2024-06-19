import os

from unittest import TestCase

from ssd.ssd import SSD


class TestSSD(TestCase):
    def setUp(self):
        super().setUp()
        self.__ssd = SSD()

    def test_out_of_range_lba_write(self):
        out_of_range_lbas = (-100, -3, -1, 100, 111, 145)
        for lba in out_of_range_lbas:
            with self.assertRaises(ValueError):
                self.__ssd.write(lba, 0x100)

    def test_mismatch_type_lba_write(self):
        invalid_lbas = ("x", None)
        for lba in invalid_lbas:
            with self.assertRaises(TypeError):
                self.__ssd.write(lba, 0x100)

    def test_out_of_range_val_write(self):
        out_of_range_vals = (-0x10, -0x1, 0x100000000, 0x123456789, 0xABCDABCD0)
        for val in out_of_range_vals:
            with self.assertRaises(ValueError):
                self.__ssd.write(0x0, val)

    def test_mismatch_type_val_write(self):
        invalid_vals = ("x", None)
        for val in invalid_vals:
            with self.assertRaises(TypeError):
                self.__ssd.write(0x0, val)

    def test_successful_write(self):
        for edge_lba in (0, 99):
            for edge_val in (0, 0xFFFFFFFF):
                self.__ssd.write(edge_lba, edge_val)

        for lba in range(0, 100, 20):
            for val in range(0, 0x100000000, 0x10000000):
                self.__ssd.write(lba, val)

    def test_successful_write_followed_by_read(self):
        for lba in range(0, 100, 20):
            for val in range(0, 0x100000000, 0x20000000):
                self.__ssd.write(lba, val)
                self.__ssd.read(lba)

                with open(self.__ssd.result_path, "r") as f:
                    try:
                        result = int(f.readline(), 16)
                    except:
                        self.fail()
                self.assertEqual(val, result)

    def test_out_of_range_lba_read(self):
        out_of_range_lbas = (-100, -3, -1, 100, 111, 145)
        for lba in out_of_range_lbas:
            with self.assertRaises(ValueError):
                self.__ssd.read(lba)

    def test_mismatch_type_lba_read(self):
        invalid_lbas = ("x", None)
        for lba in invalid_lbas:
            with self.assertRaises(TypeError):
                self.__ssd.read(lba)

    def test_read_new_ssd(self):
        tmp_nand_path = "./tmp_nand.txt"
        tmp_result_path = "./tmp_result.txt"
        tmp_ssd = SSD(tmp_nand_path, tmp_result_path)

        try:
            for lba in range(0, 100):
                tmp_ssd.read(lba)
                with open(tmp_result_path, "r") as f:
                    result = int(f.readline(), 16)
                    self.assertEqual(0, result)
        finally:
            for filename in (tmp_result_path, tmp_nand_path):
                try:
                    os.remove(filename)
                except OSError:
                    pass
