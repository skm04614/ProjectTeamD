from custom_ssd.cssd import TARGET_SSD


def tc_fullread_10_compare() -> bool:
    try:
        test_count = 10
        compare = ""
        for _ in range(test_count):
            results = []
            for lba in range(TARGET_SSD.LBA_LOWER_BOUND, TARGET_SSD.LBA_UPPER_BOUND + 1):
                command = TARGET_SSD.command_factory("R", lba)
                TARGET_SSD.queue_command(command)
                results.append(TARGET_SSD.custom_os.read_from_memory())
            if not compare:
                compare = "\n".join(results)
                continue
            assert compare == "\n".join(results)
    except:
        return False
    else:
        return True
