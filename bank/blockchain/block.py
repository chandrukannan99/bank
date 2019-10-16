from datetime import datetime
from crypto.utils import sha512
from crypto.utils import merkle_root
from blockchain import Transaction
from base64 import b64encode


class Block:

    def __init__(self, previous_hash):

        self.previous_hash = previous_hash
        self.nonce = 0
        self.timestamp = datetime.now().timestamp()
        self.transactions = []
        self.merkle_root = self.get_merkle_root()
        self.hash = self.calculate_hash()

    def get_message(self):
        return self.previous_hash + str(self.nonce) + str(self.timestamp) + self.merkle_root

    def calculate_hash(self):

        message = self.get_message()
        return sha512(message)

    def mine(self, difficulty=5):

        hash_prefix = '0' * difficulty

        while not self.hash.startswith(hash_prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def get_merkle_root(self) -> str:
        transaction_ids = [transaction.transaction_id for transaction in self.transactions]
        return merkle_root(transaction_ids)

    def add_transaction(self, transaction, all_utxos, minimum_transaction) -> bool:
        if transaction is None:
            return False

        # process transaction and check if valid, unless block is genesis block then ignore.
        if self.previous_hash != "0":
            if not transaction.process_transaction(all_utxos, minimum_transaction):
                print("Transaction failed to process")
                return False

        self.transactions.append(transaction)
        return True

    def __str__(self):
        return self.hash

    def print(self):
        print("hash:", self.hash)
        print("transactions_count", len(self.transactions))

        for i in range(len(self.transactions)):
            t = self.transactions[i]
            print("  Transaction %d" % i)
            print("    id: %s" % t.transaction_id)
            print("    sender: %s" % t.sender)
            print("    recipient: %s" % t.recipient)
            print("    signature: %s" % t.get_signature_as_str())

        print("merkle_root:", self.merkle_root)
        print("timestamp:", self.timestamp)
        print("nonce:", self.nonce)
        print("prev_hash:", self.previous_hash)
        print()

    @classmethod
    def deserialize(cls, info: dict):

        block = Block('')
        block.hash = info['hash']
        block.previous_hash = info['prev_block']
        block.nonce = info['nonce']
        block.timestamp = info['time_stamp']
        block.merkle_root = info['merkle_root']
        block.transactions = []

        for transaction_data in info['transactions']:
            block.transactions.append(Transaction.deserialize(transaction_data))

        return block
