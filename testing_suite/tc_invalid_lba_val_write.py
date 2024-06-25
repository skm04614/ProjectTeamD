from custom_ssd.cssd import TARGET_SSD


def tc_invalid_lba_val_write():
    invalid_lbas = (TARGET_SSD.LBA_LOWER_BOUND - 1, TARGET_SSD.LBA_UPPER_BOUND + 1)
    invalid_vals = ("0x100000000", "0x1234")

    for lba in invalid_lbas:
        for val in invalid_vals:
            try:
                TARGET_SSD.queue_command(TARGET_SSD.command_factory("W", lba, val))
            except ValueError:
                pass
            else:
                raise AssertionError("Value Error must have occurred.")
