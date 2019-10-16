import peewee

from crypto.utils import sha512
from models import BaseModel, Wallet


class User(BaseModel):

    username = peewee.CharField(max_length=64, unique=True)
    secret = peewee.CharField()

    is_superuser = peewee.BooleanField(default=False)

    wallet = peewee.ForeignKeyField(Wallet, backref='owner', unique=True)

    def set_password(self, password):
        self.secret = User.get_hash_of_password(self.username, password)

    def check_password(self, password):
        return self.secret == User.get_hash_of_password(self.username, password)

    def __str__(self):
        return self.username

    @staticmethod
    def get_hash_of_password(username, password):
        return sha512(username + password)

    @staticmethod
    def create_user(username, password):
        wallet = Wallet.create_wallet(password)
        user = User(username=username, wallet=wallet)
        user.set_password(password)

        try:
            user.save()
        except Exception as e:
            wallet.delete()

            raise e

        return user
