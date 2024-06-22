from custom_ssd.cssd import SSD


def tc_app_1() -> bool:
    ssd = SSD()

    target_val = "0x1234ABCD"

    try:
        for lba in range(ssd.LBA_LOWER_BOUND, ssd.LBA_UPPER_BOUND + 1):
            command = ssd.command_factory("W", lba, target_val)
            ssd.queue_command(command)

        for lba in range(ssd.LBA_LOWER_BOUND, ssd.LBA_UPPER_BOUND + 1):
            command = ssd.command_factory("R", lba)
            ssd.queue_command(command)

            assert ssd.custom_os.read_from_memory() == target_val
    except:
        return False
    else:
        return True
