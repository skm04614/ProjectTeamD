from custom_ssd.cssd import SSD


def tc_app_2() -> bool:
    ssd = SSD()

    target_val = "0xAAAABBBB"
    target_lbas = tuple(range(0, 5 + 1))

    try:
        for _ in range(30):
            for lba in target_lbas:
                command = ssd.command_factory("W", lba, target_val)
                ssd.queue_command(command)

        target_val = "0x12345678"
        for lba in target_lbas:
            command = ssd.command_factory("W", lba, target_val)
            ssd.queue_command(command)

        for lba in target_lbas:
            command = ssd.command_factory("R", lba)
            ssd.queue_command(command)

            assert ssd.custom_os.read_from_memory() == target_val
    except:
        return False
    else:
        return True
