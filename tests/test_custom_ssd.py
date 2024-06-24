import os
import itertools
from unittest.mock import Mock

import numpy as np
from unittest import TestCase

from custom_ssd.cssd import SSD


class TestSSD(TestCase):
    def setUp(self):
        super().setUp()

        self.__test_nand_path = os.path.join(os.path.dirname(__file__), "test_nand.txt")
        self.__test_buffer_path = os.path.join(os.path.dirname(__file__), "test_buffer.txt")
        self.__ssd = SSD(self.__test_nand_path,
                         self.__test_buffer_path)

        self._valid_lbas = tuple(int(lba) for lba in np.linspace(self.__ssd.LBA_LOWER_BOUND,
                                                                 self.__ssd.LBA_UPPER_BOUND,
                                                                 7))

        self._valid_vals = ("0x00000000", "0x12345678", "0x33334444", "0x98765432",
                            "0xA1B2C3D4", "0xAFBECDAF", "0xFFFFFFFF")

        self._invalid_lbas = (-100, -1, 100, 150)
        self._wrong_typed_lbas = ([], None, "1b", "a1")
        self._invalid_vals = ("0x0", "0x1234", "FFFF0000", "0x100000000", "-0x12345678")
        self._wrong_typed_vals = ([], None, 0xFFFFFFFF, 0x0)

    def tearDown(self):
        for test_path in (self.__test_buffer_path, self.__test_nand_path):
            try:
                os.remove(test_path)
            except OSError:
                pass

    def test_invalid_lba_write(self):
        for lba in self._invalid_lbas:
            with self.assertRaises(ValueError):
                self.__ssd.command_factory("W", lba, self._valid_vals[0]).execute()

    def test_mismatch_type_write(self):
        for lba in self._wrong_typed_lbas:
            with self.assertRaises(TypeError):
                self.__ssd.command_factory("W", lba, self._valid_vals[0]).execute()

        for val in self._wrong_typed_vals:
            with self.assertRaises(ValueError):
                self.__ssd.command_factory("W", self._valid_lbas[0], val).execute()

    def test_invalid_val_write(self):
        for val in self._invalid_vals:
            with self.assertRaises(ValueError):
                self.__ssd.command_factory("W", self._valid_lbas[0], val).execute()

    def test_successful_write(self):
        for args in itertools.product(self._valid_lbas, self._valid_vals):
            self.__ssd.command_factory("W", *args).execute()

    def test_aging_write_followed_by_read(self):
        lba = self._valid_lbas[2]
        val = self._valid_vals[3]

        for _ in range(100):
            self.__ssd.command_factory("W", lba, val).execute()

        self.__ssd.command_factory("R", lba).execute()
        self.assertEqual(val, self.__ssd.custom_os.read_from_memory())

    def test_successful_write_followed_by_read(self):
        for args in itertools.product(self._valid_lbas, self._valid_vals):
            self.__ssd.command_factory("W", *args).execute()
            self.__ssd.command_factory("R", args[0]).execute()
            self.assertEqual(args[1], self.__ssd.custom_os.read_from_memory())

    def test_invalid_lba_read(self):
        for lba in self._invalid_lbas:
            with self.assertRaises(ValueError):
                self.__ssd.command_factory("R", lba).execute()

    def test_mismatch_type_read(self):
        for lba in self._wrong_typed_lbas:
            with self.assertRaises(TypeError):
                self.__ssd.command_factory("R", lba).execute()

    def test_read_new_ssd_by_mock(self):
        ssd = SSD(self.__test_nand_path,
                  self.__test_buffer_path,
                  Mock())
        expected_val = "0x1234FFFF"
        ssd.custom_os.read_from_memory.return_value = expected_val

        for lba in range(ssd.LBA_LOWER_BOUND, ssd.LBA_UPPER_BOUND + 1):
            ssd.command_factory("R", lba).execute()
            self.assertEqual(expected_val, ssd.custom_os.read_from_memory())

    def test_read_new_ssd(self):
        for lba in range(self.__ssd.LBA_LOWER_BOUND, self.__ssd.LBA_UPPER_BOUND + 1):
            self.__ssd.command_factory("R", lba).execute()
            self.assertEqual("0x00000000", self.__ssd.custom_os.read_from_memory())

    def test_mismatch_type_erase(self):
        for lba in self._wrong_typed_lbas:
            with self.assertRaises(TypeError):
                self.__ssd.command_factory("E", lba, 1).execute()

        for size in (None, []):
            with self.assertRaises(TypeError):
                self.__ssd.command_factory("E", self._valid_lbas[0], size).execute()

    def test_invalid_start_lba_erase(self):
        for lba in self._invalid_lbas:
            with self.assertRaises(ValueError):
                self.__ssd.command_factory("E", lba, 5).execute()

    def test_invalid_end_lba_erase(self):
        for lba in (98, 110, 99, 91):
            with self.assertRaises(ValueError):
                self.__ssd.command_factory("E", lba, 10).execute()

    def test_invalid_size_erase(self):
        for size in (-1, -10, 11, 20, 0):
            with self.assertRaises(ValueError):
                self.__ssd.command_factory("E", self._valid_lbas[0], size).execute()

    def test_successful_erase_verify(self):
        for lba in range(0, 100):
            self.__ssd.command_factory("W", lba, "0x12345678").execute()

        for args in ((0, 10), (2, 10), (2, 5), (14, 10), (90, 10), (27, 5), (31, 9), (99, 1)):
            self.__ssd.command_factory("E", *args).execute()

            start_lba = args[0]
            end_lba = sum(args) - 1
            for lba in range(start_lba, end_lba + 1):
                self.__ssd.command_factory("R", lba).execute()
                self.assertEqual("0x00000000", self.__ssd.custom_os.read_from_memory())

    def test_empty_flush(self):
        self.__ssd.queue_command(self.__ssd.command_factory("F"))

        self.assertEqual(0, len(self.__ssd._command_buffer))

        for lba in range(self.__ssd.LBA_LOWER_BOUND, self.__ssd.LBA_UPPER_BOUND + 1):
            self.assertEqual("0x00000000", self.__ssd._nand_data[lba])

    def test_flush(self):
        expected_vals = ["0x00000000" for _ in range(self.__ssd.LBA_LOWER_BOUND,
                                                     self.__ssd.LBA_UPPER_BOUND + 1)]

        self.__ssd.queue_command(self.__ssd.command_factory("W", 3, "0x12345678"))
        self.__ssd.queue_command(self.__ssd.command_factory("W", 7, "0x87654321"))
        self.__ssd.queue_command(self.__ssd.command_factory("W", 11, "0x99999999"))

        self.assertEqual(3, len(self.__ssd._command_buffer))
        self.assertEqual("0x12345678", self.__ssd.search(3))
        self.assertEqual("0x87654321", self.__ssd.search(7))
        self.assertEqual("0x99999999", self.__ssd.search(11))
        for lba, expected_val in enumerate(expected_vals):
            self.assertEqual(expected_val, self.__ssd._nand_data[lba])

        self.__ssd.queue_command(self.__ssd.command_factory("F"))
        self.assertEqual(0, len(self.__ssd._command_buffer))
        expected_vals[3] = "0x12345678"
        expected_vals[7] = "0x87654321"
        expected_vals[11] = "0x99999999"

        for lba, expected_val in enumerate(expected_vals):
            self.assertEqual(expected_val, self.__ssd._nand_data[lba])
