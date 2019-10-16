from crypto.utils import sha512


class TransactionOutput:
    """
    The result of doing a transaction
    """

    def __init__(self, recipient_public_key_str: str, value: float, parent_transaction_id: str):
        self.recipient = recipient_public_key_str
        self.value = value
        self.parent_transaction_id = parent_transaction_id
        self.id = self.calculate_hash()

    def calculate_hash(self):
        message = self.recipient + str(self.value) + self.parent_transaction_id
        return sha512(message)

    def is_mine(self, public_key_str):
        return self.recipient == public_key_str

    @classmethod
    def deserialize(cls, info: dict):
        recipient_public_key = info['recipient_public_key']
        value = info['value']
        parent_transaction_id = info['parent_transaction_id']

        output = TransactionOutput(recipient_public_key, value, parent_transaction_id)
        output.id = info['id']

        return output
