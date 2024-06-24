from time import sleep


def tc_fail() -> None:
    sleep(1.5)

    raise AssertionError("This tc is designed to fail")
