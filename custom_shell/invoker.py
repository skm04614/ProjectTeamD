from custom_shell.command_interface import ICommand


def invoke_command(command: ICommand) -> None:
    command.execute()
