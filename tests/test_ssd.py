import os

from unittest import TestCase

from custom_ssd.ssd import SSD


class TestSSD(TestCase):
    def setUp(self):
        super().setUp()
        nand_path = os.path.join(os.path.dirname(__file__), "test_nand.txt")
        result_path = os.path.join(os.path.dirname(__file__), "test_result.txt")
        self.__ssd = SSD(nand_path, result_path)

    def tearDown(self):
        try:
            os.remove(self.__ssd.nand_path)
        except OSError:
            pass

        try:
            os.remove(self.__ssd.result_path)
        except OSError:
            pass

    def test_out_of_range_lba_write(self):
        out_of_range_lbas = (-100, -3, -1, 100, 111, 145)
        for lba in out_of_range_lbas:
            with self.assertRaises(ValueError):
                self.__ssd.write(lba, "0x00000100")

    def test_mismatch_type_lba_write(self):
        invalid_lbas = ("x", None)
        for lba in invalid_lbas:
            with self.assertRaises(TypeError):
                self.__ssd.write(lba, "0x00000100")

    def test_out_of_range_val_write(self):
        out_of_range_vals = ("-0x10", "-0x1", "0x100000000", "0x123456789", "0xABCDABCD0", "0x1234", "0xFFFFFF")
        for val in out_of_range_vals:
            with self.assertRaises(ValueError):
                self.__ssd.write(0x0, val)

    def test_mismatch_type_val_write(self):
        invalid_vals = (1234, None)
        for val in invalid_vals:
            with self.assertRaises(TypeError):
                self.__ssd.write(0x0, val)

    def test_successful_write(self):
        for lba in (0, 35, 99):
            for val in ("0x00000000", "0x12345678", "0xFFFFFFFF"):
                self.__ssd.write(lba, val)

    def test_successful_write_followed_by_read(self):
        for lba in (0, 35, 99):
            for val in ("0x00000000", "0x12345678", "0xFFFFFFFF"):
                self.__ssd.write(lba, val)
                self.__ssd.read(lba)

                with open(self.__ssd.result_path, "r") as f:
                    try:
                        result = f.readline()
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
        for lba in range(0, 100):
            self.__ssd.read(lba)
            with open(self.__ssd.result_path, "r") as f:
                result = int(f.readline(), 16)
                self.assertEqual(0, result)

    def test_mismatch_type_erase(self):
        error_typed_values = ("x", None)
        for val in error_typed_values:
            with self.assertRaises(TypeError):
                self.__ssd.erase(val, 10)
            with self.assertRaises(TypeError):
                self.__ssd.erase(0, val)

    def test_out_of_range_start_lba_erase(self):
        out_of_range_lbas = (-1, 100, 150, -10)
        for lba in out_of_range_lbas:
            with self.assertRaises(ValueError):
                self.__ssd.erase(lba, 5)

    def test_out_of_range_end_lba_erase(self):
        start_lbas = (98, 110, 99, 91)
        for lba in start_lbas:
            with self.assertRaises(ValueError):
                self.__ssd.erase(lba, 10)

    def test_out_of_range_size_erase(self):
        invalid_sizes = (-1, -10, 11, 20, 0)
        for size in invalid_sizes:
            with self.assertRaises(ValueError):
                self.__ssd.erase(50, size)

    def test_successful_erase_verify(self):
        for lba in range(0, 100):
            self.__ssd.write(lba, "0x12345678")

        valid_args = ((0, 10), (2, 10), (90, 10), (27, 5), (31, 9), (99, 1))
        for args in valid_args:
            self.__ssd.erase(*args)

            start_lba = args[0]
            end_lba = sum(args) - 1
            for lba in range(start_lba, end_lba + 1):
                self.__ssd.read(lba)
                with open(self.__ssd.result_path, "r") as f:
                    self.assertEqual("0x00000000", f.readline())
