import shlex

from cli import command_provider, ValidationError
from auth import Auth
from blockchain_handler import blockchain_handler

blockchain_handler.load_blockchain()


def get_command_prefix():
    user = Auth.get_user()

    if user:
        return user.username + ' $ '

    else:
        return '$ '


if __name__ == '__main__':

    command_provider.credit_command.run()

    while not command_provider.exit_command.exit:

        _input = input(get_command_prefix())
        parts = shlex.split(_input)

        if not parts:
            continue

        for command in command_provider.get_commands():
            prefix_len = command.has_prefix(parts)

            if prefix_len < 0:
                continue

            params = parts[prefix_len:]

            try:
                command.validate_params(params)
                command.run(*params)

            except ValidationError as e:
                print("Error: " + str(e))
                print(command.get_description())

            except Exception as e:
                print("Error: " + str(e))

            break

        else:
            print("Error: No such command found. Please type `help`.")
