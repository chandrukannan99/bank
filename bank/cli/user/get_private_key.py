from cli.user import UserBaseCommand
from auth import Auth


class GetPrivateKeyCommand(UserBaseCommand):

    prefix_list = ('get', 'private', 'key')

    def run(self):
        user = Auth.get_user()

        private_key = user.wallet.get_private_key_str()

        print(private_key)

        return private_key
