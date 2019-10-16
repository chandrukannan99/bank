import random
import string

import peewee

from models import BaseModel, CentralBank


def token_default():
    N = 128
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


class BankToken(BaseModel):
    token = peewee.CharField(default=token_default)
    central_bank = peewee.ForeignKeyField(CentralBank)
