from custom_ssd.cssd import TARGET_SSD


def tc_fullread_10_compare() -> bool:
    try:
        compare = ""
        for lba in range(TARGET_SSD.LBA_LOWER_BOUND, TARGET_SSD.LBA_UPPER_BOUND + 1):
            command = TARGET_SSD.command_factory("R", lba)
            TARGET_SSD.queue_command(command)
            if not compare:
                compare = TARGET_SSD.custom_os.read_from_memory()
                continue
            assert TARGET_SSD.custom_os.read_from_memory() == compare
    except:
        return False
    else:
        return True