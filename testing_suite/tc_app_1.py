from custom_ssd.cssd import TARGET_SSD


def tc_app_1() -> bool:
    target_val = "0x1234ABCD"

    try:
        for lba in range(TARGET_SSD.LBA_LOWER_BOUND, TARGET_SSD.LBA_UPPER_BOUND + 1):
            command = TARGET_SSD.command_factory("W", lba, target_val)
            TARGET_SSD.queue_command(command)

        for lba in range(TARGET_SSD.LBA_LOWER_BOUND, TARGET_SSD.LBA_UPPER_BOUND + 1):
            command = TARGET_SSD.command_factory("R", lba)
            TARGET_SSD.queue_command(command)

            assert TARGET_SSD.custom_os.read_from_memory() == target_val
    except:
        return False
    else:
        return True
