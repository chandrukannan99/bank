import peewee

from models import BaseModel, User, Bank


class Customer(BaseModel):

    user = peewee.ForeignKeyField(User, unique=True)
    bank = peewee.ForeignKeyField(Bank)
