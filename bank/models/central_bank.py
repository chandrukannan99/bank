import peewee

from models import BaseModel, User


class CentralBank(BaseModel):

    manager = peewee.ForeignKeyField(User, backref='central_bank', unique=True)

    number_of_transactions_in_block = peewee.SmallIntegerField(default=0)
    transaction_fee = peewee.FloatField(default=0)
    block_miner_reward = peewee.FloatField(default=0)
    difficulty = peewee.SmallIntegerField(default=0)
    bank_balance_min_percent_for_loan = peewee.FloatField(default=0)

    def has_valid_configuration(self):
        # from blockchain_handler import blockchain_handler

        return self.number_of_transactions_in_block > 0 \
               and self.transaction_fee > 0 \
               and self.block_miner_reward > 0 \
               and self.difficulty > 0 \
               and self.bank_balance_min_percent_for_loan > 0 \
               # and blockchain_handler.is_blockchain_imported()

    @staticmethod
    def get_central_bank():
        return CentralBank.select().first()
