from random import sample

from custom_ssd.cssd import TARGET_SSD


def tc_write_10_times_and_compare() -> None:
    test_count = 10
    target_lbas = sample(range(TARGET_SSD.LBA_LOWER_BOUND, TARGET_SSD.LBA_UPPER_BOUND + 1), test_count)
    target_vals = [f"0x{n:08X}" for n in sample(range(TARGET_SSD.VAL_LOWER_BOUND, TARGET_SSD.VAL_UPPER_BOUND + 1), test_count)]

    for lba, val in zip(target_lbas, target_vals):
        command = TARGET_SSD.command_factory("W", lba, val)
        TARGET_SSD.queue_command(command)

    for lba, val in zip(target_lbas, target_vals):
        command = TARGET_SSD.command_factory("R", lba)
        TARGET_SSD.queue_command(command)
        assert TARGET_SSD.custom_os.read_from_memory() == val
