from cli.user import UserBaseCommand
from auth import Auth


class GetPublicKeyCommand(UserBaseCommand):

    prefix_list = ('get', 'public', 'key')

    def run(self):
        user = Auth.get_user()

        public_key = user.wallet.public_key_str

        print(public_key)

        return public_key
