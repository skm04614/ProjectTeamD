from random import randint

from custom_ssd.cssd import TARGET_SSD


def tc_loop_write_and_read_compare() -> None:
    loop_count = 100
    target_val = f"0x{randint(0, 0xFFFFFFFF):08X}"
    for _ in range(loop_count):
        target_lba = randint(TARGET_SSD.LBA_LOWER_BOUND, TARGET_SSD.LBA_UPPER_BOUND)
        TARGET_SSD.queue_command(TARGET_SSD.command_factory("W", target_lba, target_val))
        TARGET_SSD.queue_command(TARGET_SSD.command_factory("R", target_lba))
        assert TARGET_SSD.custom_os.read_from_memory() == target_val
