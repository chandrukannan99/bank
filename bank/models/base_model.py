import peewee

vbank_db = peewee.SqliteDatabase('resources/vbank.db')


class BaseModel(peewee.Model):

    class Meta:
        database = vbank_db
