from custom_ssd.cssd import SSD
from random import randint


def tc_single_random_lba_val_write_compare() -> bool:
    ssd = SSD()

    target_val = f"0x{randint(0, 0xFFFFFFFF):08X}"
    target_lba = randint(ssd.LBA_LOWER_BOUND, ssd.LBA_UPPER_BOUND)

    try:
        command = ssd.command_factory("W", target_lba, target_val)
        ssd.queue_command(command)

        command = ssd.command_factory("R", target_lba)
        ssd.queue_command(command)

        assert ssd.custom_os.read_from_memory() == target_val
    except:
        return False
    else:
        return True
