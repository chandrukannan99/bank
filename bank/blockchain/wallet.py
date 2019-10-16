from typing import Dict

from Crypto.PublicKey.RSA import RsaKey
from crypto.rsa import one_line_format
from blockchain import TransactionOutput, Transaction, TransactionInput


class Wallet:

    def __init__(self):
        self.public_key_str = None  # type: str
        self.private_key = None  # type: RsaKey

        self.utxos = {}  # type: Dict[str, TransactionOutput]

    def private_key_as_str(self):
        return one_line_format(self.private_key.export_key().decode())

    def print(self):
        print("Public key: " + self.public_key_str)
        print("Private key: " + self.private_key_as_str())

    def get_balance(self, all_utxos):
        self.update_utxos(all_utxos)

        amount = 0

        for utxo in self.utxos.values():
            amount += utxo.value

        return amount

    def update_utxos(self, all_utxos):
        self.utxos = {}
        my_public_key = self.public_key_str

        for output_id, utxo in all_utxos.items():
            if utxo.is_mine(my_public_key):
                self.utxos[output_id] = utxo

    def send_funds(self, all_utxos, recipient_public_key_str: str, value: float) -> Transaction:
        self.update_utxos(all_utxos)

        if self.get_balance(all_utxos) < value:
            raise Exception("Not enough balance, transaction discarded")

        if value <= 0:
            raise Exception("Value should be positive, transaction discarded")

        inputs = []
        total = 0
        for transaction_id, utxo in self.utxos.items():
            total += utxo.value
            inp = TransactionInput(transaction_id)
            inputs.append(inp)

            if total >= value:
                break

        transaction = Transaction(self.public_key_str, recipient_public_key_str, value, inputs)
        transaction.generate_signature(self.private_key)

        for inp in inputs:
            del self.utxos[inp.transaction_output_id]

        return transaction
