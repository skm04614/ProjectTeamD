from custom_ssd.cssd import TARGET_SSD
from random import randint


def tc_single_random_lba_val_write_compare() -> None:
    target_val = f"0x{randint(0, 0xFFFFFFFF):08X}"
    target_lba = randint(TARGET_SSD.LBA_LOWER_BOUND, TARGET_SSD.LBA_UPPER_BOUND)

    command = TARGET_SSD.command_factory("W", target_lba, target_val)
    TARGET_SSD.queue_command(command)

    command = TARGET_SSD.command_factory("R", target_lba)
    TARGET_SSD.queue_command(command)

    assert TARGET_SSD.custom_os.read_from_memory() == target_val
