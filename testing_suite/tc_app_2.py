from custom_ssd.cssd import TARGET_SSD


def tc_app_2() -> None:
    target_val = "0xAAAABBBB"
    target_lbas = tuple(range(0, 5 + 1))

    for _ in range(30):
        for lba in target_lbas:
            command = TARGET_SSD.command_factory("W", lba, target_val)
            TARGET_SSD.queue_command(command)

    target_val = "0x12345678"
    for lba in target_lbas:
        command = TARGET_SSD.command_factory("W", lba, target_val)
        TARGET_SSD.queue_command(command)

    for lba in target_lbas:
        command = TARGET_SSD.command_factory("R", lba)
        TARGET_SSD.queue_command(command)

        assert TARGET_SSD.custom_os.read_from_memory() == target_val
