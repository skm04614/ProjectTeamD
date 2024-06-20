import os
import itertools
import numpy as np
from unittest import TestCase

from custom_ssd.cssd import SSD


class TestSSD(TestCase):
    def setUp(self):
        super().setUp()
        test_nand_path = os.path.join(os.path.dirname(__file__), "test_nand.txt")
        self.__ssd = SSD(test_nand_path)

        self._valid_lbas = tuple(int(lba) for lba in np.linspace(self.__ssd.LBA_LOWER_BOUND,
                                                                 self.__ssd.LBA_UPPER_BOUND,
                                                                 7))

        self._valid_vals = tuple(f"0x{int(val):08X}" for val in np.linspace(self.__ssd.VAL_LOWER_BOUND,
                                                                            self.__ssd.VAL_UPPER_BOUND,
                                                                            7))

        self._invalid_lbas = (-100, -1, 100, 150)
        self._wrong_typed_lbas = ([], None, "0", "1b", "a1")
        self._invalid_vals = ("0x0", "0x1234", "FFFF0000", "0x100000000", "-0x12345678")
        self._wrong_typed_vals = ([], None, 0xFFFFFFFF, 0x0)

    def tearDown(self):
        try:
            os.remove(self.__ssd.nand_path)
        except OSError:
            pass

    def test_invalid_lba_write(self):
        for lba in self._invalid_lbas:
            with self.assertRaises(ValueError):
                self.__ssd.write(lba, self._valid_vals[0])

    def test_mismatch_type_write(self):
        for lba in self._wrong_typed_lbas:
            with self.assertRaises(TypeError):
                self.__ssd.write(lba, self._valid_vals[0])

        for val in self._wrong_typed_vals:
            with self.assertRaises(TypeError):
                self.__ssd.write(self._valid_lbas[0], val)

    def test_invalid_val_write(self):
        for val in self._invalid_vals:
            with self.assertRaises(ValueError):
                self.__ssd.write(self._valid_lbas[0], val)

    def test_successful_write(self):
        for args in itertools.product(self._valid_lbas, self._valid_vals):
            self.__ssd.write(*args)

    def test_aging_write_followed_by_read(self):
        lba = self._valid_lbas[2]
        val = self._valid_vals[3]

        for _ in range(100):
            self.__ssd.write(lba, val)

        self.__ssd.read(lba)
        self.assertEqual(val, self.__ssd.custom_os.read_from_memory())

    def test_successful_write_followed_by_read(self):
        for args in itertools.product(self._valid_lbas, self._valid_vals):
            self.__ssd.write(*args)
            self.__ssd.read(args[0])
            self.assertEqual(args[1], self.__ssd.custom_os.read_from_memory())

    def test_invalid_lba_read(self):
        for lba in self._invalid_lbas:
            with self.assertRaises(ValueError):
                self.__ssd.read(lba)

    def test_mismatch_type_read(self):
        for lba in self._wrong_typed_lbas:
            with self.assertRaises(TypeError):
                self.__ssd.read(lba)

    def test_read_new_ssd(self):
        for lba in range(self.__ssd.LBA_LOWER_BOUND, self.__ssd.LBA_UPPER_BOUND):
            self.__ssd.read(lba)
            self.assertEqual("0x00000000", self.__ssd.custom_os.read_from_memory())

    def test_mismatch_type_erase(self):
        for lba in self._wrong_typed_lbas:
            with self.assertRaises(TypeError):
                self.__ssd.erase(lba, 1)

        for size in (None, [], "5"):
            with self.assertRaises(TypeError):
                self.__ssd.erase(self._valid_lbas[0], size)

    def test_invalid_start_lba_erase(self):
        for lba in self._invalid_lbas:
            with self.assertRaises(ValueError):
                self.__ssd.erase(lba, 5)

    def test_invalid_end_lba_erase(self):
        for lba in (98, 110, 99, 91):
            with self.assertRaises(ValueError):
                self.__ssd.erase(lba, 10)

    def test_invalid_size_erase(self):
        for size in (-1, -10, 11, 20, 0):
            with self.assertRaises(ValueError):
                self.__ssd.erase(self._valid_lbas[0], size)

    def test_successful_erase_verify(self):
        for lba in range(0, 100):
            self.__ssd.write(lba, "0x12345678")

        for args in ((0, 10), (2, 10), (2, 5), (14, 10), (90, 10), (27, 5), (31, 9), (99, 1)):
            self.__ssd.erase(*args)

            start_lba = args[0]
            end_lba = sum(args) - 1
            for lba in range(start_lba, end_lba + 1):
                self.__ssd.read(lba)
                self.assertEqual("0x00000000", self.__ssd.custom_os.read_from_memory())