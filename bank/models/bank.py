import peewee

from models import BaseModel, User, BankToken


class Bank(BaseModel):

    manager = peewee.ForeignKeyField(User, unique=True)

    bank_name = peewee.CharField(unique=True)

    bank_token = peewee.ForeignKeyField(BankToken, unique=True)
