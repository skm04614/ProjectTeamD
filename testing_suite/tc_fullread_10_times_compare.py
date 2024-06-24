from custom_ssd.cssd import TARGET_SSD


def tc_fullread_10_times_compare() -> bool:
    expected = None
    try:
        for _ in range(10):
            result = []
            for lba in range(TARGET_SSD.LBA_LOWER_BOUND, TARGET_SSD.LBA_UPPER_BOUND + 1):
                command = TARGET_SSD.command_factory("R", lba)
                TARGET_SSD.queue_command(command)
                result.append(TARGET_SSD.custom_os.read_from_memory())

            if expected is None:
                expected = result

            assert expected == result
    except:
        return False
    else:
        return True
