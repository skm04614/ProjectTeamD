import os
from unittest import TestCase

from custom_ssd.cssd import SSD
from custom_ssd.command import *


class TestSSD(TestCase):
    def setUp(self):
        super().setUp()

        self.__test_nand_path = os.path.join(os.path.dirname(__file__), "test_nand.txt")
        self.__test_buffer_path = os.path.join(os.path.dirname(__file__), "test_buffer.txt")
        self.__ssd = SSD(self.__test_nand_path,
                         self.__test_buffer_path)

        self.__command_buffer = self.__ssd._command_buffer

        for lba in range(self.__ssd.LBA_LOWER_BOUND,
                         self.__ssd.LBA_UPPER_BOUND + 1):
            self.__ssd.command_factory("W", lba, "0xFFFFFFFF").execute()

    def tearDown(self):
        with open(self.__test_buffer_path, "r") as f:
            for command in self.__command_buffer:
                self.assertEqual(str(command), f.readline().strip())
            self.assertEqual("", f.read().strip())

        for test_path in (self.__test_buffer_path, self.__test_nand_path):
            try:
                os.remove(test_path)
            except OSError:
                pass

    def test_queue_k_write_commands_with_consecutive_lbas(self):
        k = self.__command_buffer.MAX_SIZE - 1

        lbas = tuple(range(0, k))
        vals = tuple(f"0x{n:08X}" for n in range(0x12345678, 0x12345678 + k))

        for n, args in enumerate(zip(lbas, vals), 1):
            self.__command_buffer.push(self.__ssd.command_factory("W", *args))
            self.assertEqual(n, len(self.__command_buffer))

        for command, lba, val in zip(iter(self.__command_buffer), lbas, vals):
            self.assertIsInstance(command, WriteCommand)
            self.assertEqual(command.start_lba, command.end_lba)
            self.assertEqual(command.start_lba, lba)
            self.assertEqual(command.val, val)

        with open(self.__test_nand_path, "r") as f:
            for lba, line in enumerate(f):
                self.assertEqual(line.strip(), "0xFFFFFFFF")
            self.assertEqual("", f.read().strip())

    def test_queue_k_write_commands_on_same_lba(self):
        k = self.__command_buffer.MAX_SIZE - 1

        lba = 0
        vals = tuple(f"0x{n:08X}" for n in range(0x12345678, 0x12345678 + k))

        for val in vals:
            self.__command_buffer.push(self.__ssd.command_factory("W", lba, val))
            self.assertEqual(1, len(self.__command_buffer))

        command = self.__command_buffer[0]
        self.assertIsInstance(command, WriteCommand)
        self.assertEqual(command.start_lba, command.end_lba)
        self.assertEqual(command.start_lba, lba)
        self.assertEqual(command.val, vals[-1])

        with open(self.__test_nand_path, "r") as f:
            for lba, line in enumerate(f):
                self.assertEqual(line.strip(), "0xFFFFFFFF")
            self.assertEqual("", f.read().strip())

    def test_ignore_write_1(self):
        lbas = (20, 21, 20)
        vals = ("0xABCDABCD", "0x12341234", "0xEEEEFFFF")

        expected_sizes = (1, 2, 2)
        for expected_size, *args in zip(expected_sizes, lbas, vals):
            self.__command_buffer.push(self.__ssd.command_factory("W", *args))
            self.assertEqual(expected_size, len(self.__command_buffer))

        final_expected_lbas = (21, 20)
        final_expected_vals = ("0x12341234", "0xEEEEFFFF")
        for command, expected_lba, expected_val in zip(iter(self.__command_buffer),
                                                       final_expected_lbas,
                                                       final_expected_vals):
            self.assertIsInstance(command, WriteCommand)
            self.assertEqual(command.start_lba, command.end_lba)
            self.assertEqual(expected_lba, command.start_lba)
            self.assertEqual(expected_val, command.val)

        with open(self.__test_nand_path, "r") as f:
            for lba, line in enumerate(f):
                self.assertEqual(line.strip(), "0xFFFFFFFF")
            self.assertEqual("", f.read().strip())

    def test_ignore_write_2(self):
        self.__command_buffer.push(self.__ssd.command_factory("W", 20, "0xABCDABCD"))
        self.__command_buffer.push(self.__ssd.command_factory("W", 21, "0x12341234"))
        self.__command_buffer.push(self.__ssd.command_factory("E", 18, 5))

        self.assertEqual(1, len(self.__command_buffer))

        command = self.__command_buffer[0]
        self.assertIsInstance(command, EraseCommand)
        self.assertEqual(18, command.start_lba)
        self.assertEqual(22, command.end_lba)

    def test_merge_erase(self):
        self.__command_buffer.push(self.__ssd.command_factory("W", 20, "0xABCDABCD"))
        self.__command_buffer.push(self.__ssd.command_factory("E", 10, 2))
        self.__command_buffer.push(self.__ssd.command_factory("E", 12, 3))

        self.assertEqual(2, len(self.__command_buffer))

        command = self.__command_buffer[0]
        self.assertIsInstance(command, WriteCommand)
        self.assertEqual(command.start_lba, command.end_lba)
        self.assertEqual(20, command.start_lba)
        self.assertEqual("0xABCDABCD", command.val)

        command = self.__command_buffer[1]
        self.assertIsInstance(command, EraseCommand)
        self.assertEqual(10, command.start_lba)
        self.assertEqual(14, command.end_lba)

    def test_overflowing_merge_erase(self):
        self.__command_buffer.push(self.__ssd.command_factory("E", 10, 9))
        self.__command_buffer.push(self.__ssd.command_factory("E", 16, 7))

        self.assertEqual(len(self.__command_buffer), 2)

        command = self.__command_buffer[0]
        self.assertIsInstance(command, EraseCommand)
        self.assertEqual(10, command.start_lba)
        self.assertEqual(19, command.end_lba)

        command = self.__command_buffer[1]
        self.assertIsInstance(command, EraseCommand)
        self.assertEqual(20, command.start_lba)
        self.assertEqual(22, command.end_lba)

    def test_narrow_erase(self):
        self.__command_buffer.push(self.__ssd.command_factory("E", 10, 4))
        self.__command_buffer.push(self.__ssd.command_factory("E", 40, 5))
        self.__command_buffer.push(self.__ssd.command_factory("W", 12, "0xABCD1234"))
        self.__command_buffer.push(self.__ssd.command_factory("W", 13, "0x4BCD5351"))

        self.assertEqual(len(self.__command_buffer), 4)

        command = self.__command_buffer[0]
        self.assertIsInstance(command, EraseCommand)
        self.assertEqual(10, command.start_lba)
        self.assertEqual(11, command.end_lba)

        command = self.__command_buffer[1]
        self.assertIsInstance(command, EraseCommand)
        self.assertEqual(40, command.start_lba)
        self.assertEqual(44, command.end_lba)

        command = self.__command_buffer[2]
        self.assertIsInstance(command, WriteCommand)
        self.assertEqual(12, command.start_lba)
        self.assertEqual("0xABCD1234", command.val)

        command = self.__command_buffer[3]
        self.assertIsInstance(command, WriteCommand)
        self.assertEqual(13, command.start_lba)
        self.assertEqual("0x4BCD5351", command.val)

    def test_fast_read(self):
        for lba in range(self.__ssd.LBA_LOWER_BOUND, self.__ssd.LBA_UPPER_BOUND):
            self.__ssd.command_factory("W", lba, "0xFFFFFFFF").execute()

        self.__ssd._command_buffer.push(self.__ssd.command_factory("E", 10, 2))
        self.__command_buffer.push(self.__ssd.command_factory("W", 10, "0xABCDABCD"))
        self.__command_buffer.push(self.__ssd.command_factory("E", 12, 3))

        self.assertEqual(len(self.__command_buffer), 2)

        command = self.__command_buffer[0]
        self.assertIsInstance(command, WriteCommand)
        self.assertEqual(10, command.start_lba)
        self.assertEqual("0xABCDABCD", command.val)

        command = self.__command_buffer[1]
        self.assertIsInstance(command, EraseCommand)
        self.assertEqual(11, command.start_lba)
        self.assertEqual(14, command.end_lba)

        lbas = (8, 9, 10, 11, 12, 13, 14, 15, 16)
        expected_vals = ("0xFFFFFFFF", "0xFFFFFFFF", "0xABCDABCD", "0x00000000", "0x00000000",
                         "0x00000000", "0x00000000", "0xFFFFFFFF", "0xFFFFFFFF")

        for lba, expected_val in zip(lbas, expected_vals):
            self.assertEqual(self.__ssd.search(lba), expected_val)

    def test_flush(self):
        self.__ssd._command_buffer.push(self.__ssd.command_factory("E", 61, 7))
        self.__command_buffer.push(self.__ssd.command_factory("W", 10, "0xABCDABCD"))
        self.__command_buffer.push(self.__ssd.command_factory("W", 35, "0x1A2B9876"))

        self.assertEqual(3, len(self.__command_buffer))
        with open(self.__test_buffer_path, "r") as f:
            for command in self.__command_buffer:
                self.assertEqual(str(command), f.readline().strip())
            self.assertEqual("", f.read().strip())

        with open(self.__test_nand_path, "r") as f:
            for lba in range(self.__ssd.LBA_LOWER_BOUND,
                             self.__ssd.LBA_UPPER_BOUND + 1):
                self.assertEqual(f.readline().strip(), "0xFFFFFFFF")
            self.assertEqual("", f.read().strip())

        self.__ssd.flush_buffer()

        self.assertEqual(0, len(self.__command_buffer))
        with open(self.__test_buffer_path, "r") as f:
            self.assertEqual("", f.read().strip())

        expected_vals = ["0xFFFFFFFF" for _ in range(self.__ssd.LBA_LOWER_BOUND,
                                                     self.__ssd.LBA_UPPER_BOUND + 1)]
        expected_vals[10] = "0xABCDABCD"
        expected_vals[35] = "0x1A2B9876"
        for lba in range(61, 61 + 7):
            expected_vals[lba] = "0x00000000"

        with open(self.__test_nand_path, "r") as f:
            for expected_val in expected_vals:
                self.assertEqual(f.readline().strip(), expected_val)
            self.assertEqual("", f.read().strip())

    def test_auto_load_buffer_path(self):
        buffer_path = "test_buf_2.txt"
        nand_path = "nand_path_2.txt"

        lbas = (5, 99, 39, 17, 73)
        vals = ("0x12345678", "0xFFFFFFFF", "0xF1F2F3F4", "0xFFFF5555", "0x22AA4554")

        try:
            with open(buffer_path, "w") as f:
                for lba, val in zip(lbas, vals):
                    f.write(f"W {lba} {val}\n")

            ssd = SSD(nand_path, buffer_path)

            expected_vals = ["0x00000000" for _ in range(ssd.LBA_LOWER_BOUND,
                                                         ssd.LBA_UPPER_BOUND + 1)]
            for lba, val in zip(lbas, vals):
                expected_vals[lba] = val

            with open(nand_path, "r") as f:
                for expected_val in expected_vals:
                    self.assertEqual(f.readline().strip(), expected_val)
                self.assertEqual("", f.read().strip())
        finally:
            for path in (buffer_path, nand_path):
                try:
                    os.remove(path)
                except OSError:
                    pass

    def test_auto_flush(self):
        k = 16
        slba = 11
        lbas = tuple(range(slba, slba + k))
        val = "0x9AC8B5D7"

        for lba in lbas:
            command = self.__ssd.command_factory("W", lba, val)
            self.__ssd.queue_command(command)

        self.assertEqual(k - self.__ssd._command_buffer.MAX_SIZE, len(self.__ssd._command_buffer))
        self.assertEqual(21, self.__command_buffer[0].start_lba)

        for lba in lbas:
            self.assertEqual(val, self.__ssd.search(lba))
