from models import User
from decouple import config


def on_user_changed(user):
    from cli import command_provider
    command_provider.update(user)


class Auth:
    _user = None

    @classmethod
    def login_user(cls, username, password):

        secret = User.get_hash_of_password(username, password)
        try:
            cls._user = User.get(username=username, secret=secret)
        except User.DoesNotExist:
            raise Exception('No user exists with this username or password')

        cls._user.wallet.decrypt(password)

        on_user_changed(cls._user)

        return cls._user

    @classmethod
    def logout_user(cls):
        cls._user.wallet.truncate_keys()
        cls._user = None
        on_user_changed(cls._user)

    @classmethod
    def get_user(cls):
        return cls._user
