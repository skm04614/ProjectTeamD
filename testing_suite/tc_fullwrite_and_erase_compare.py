from random import randint

from custom_ssd.cssd import TARGET_SSD


def tc_fullwrite_and_erase_compare() -> None:
    target_val = f"0x{randint(TARGET_SSD.VAL_LOWER_BOUND, TARGET_SSD.VAL_UPPER_BOUND):08X}"
    for lba in range(TARGET_SSD.LBA_LOWER_BOUND, TARGET_SSD.LBA_UPPER_BOUND + 1):
        TARGET_SSD.queue_command(TARGET_SSD.command_factory("W", lba, target_val))

    start_lba = randint(TARGET_SSD.LBA_LOWER_BOUND, TARGET_SSD.LBA_UPPER_BOUND)
    erase_size = randint(TARGET_SSD.MIN_ERASE_SIZE, TARGET_SSD.MAX_ERASE_SIZE)
    if start_lba + erase_size > TARGET_SSD.LBA_UPPER_BOUND + 1:
        erase_size = TARGET_SSD.LBA_UPPER_BOUND - start_lba + 1
    TARGET_SSD.queue_command(TARGET_SSD.command_factory("E", start_lba, erase_size))

    for lba in range(start_lba, start_lba + erase_size):
        TARGET_SSD.queue_command(TARGET_SSD.command_factory("R", lba))
        assert TARGET_SSD.custom_os.read_from_memory() == TARGET_SSD.NULL
