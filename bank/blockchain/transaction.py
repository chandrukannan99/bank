from crypto.utils import sha512
from crypto.rsa import sign, verify, import_key, pem_format
from typing import List, Dict
from blockchain import TransactionOutput, TransactionInput
from base64 import b64encode

class Transaction:

    sequence = 0  # number of transactions created

    def __init__(self, from_pub_key_str: str, to_pub_key_str: str, value: float, inputs: list):
        self.sender = from_pub_key_str
        self.recipient = to_pub_key_str
        self.value = value
        self.transaction_id = None
        self.signature = None

        # transaction inputs for creating this transaction
        self.inputs = inputs  # type: List[TransactionInput]

        # transaction outputs created from this transaction
        self.outputs = []  # type: List[TransactionOutput]

    def calculate_hash(self):
        # increase the sequence to avoid 2 identical transactions having the same hash
        Transaction.sequence += 1

        message = self.sender + self.recipient + str(self.value) + str(Transaction.sequence)

        return sha512(message)

    def generate_signature(self, sender_private_key):
        message = self.sender + self.recipient + str(self.value)
        self.signature = sign(message.encode(), sender_private_key)

    def verify_signature(self):
        if not self.signature:
            return False

        message = self.sender + self.recipient + str(self.value)
        sender_public_key = import_key(pem_format(self.sender))
        return verify(message.encode(), self.signature, sender_public_key)

    def get_signature_as_str(self):
        if isinstance(self.signature, str):
            return self.signature
        else:
            return b64encode(self.signature).decode()

    def get_outputs_value(self):

        amount = 0

        for output in self.outputs:
            amount += output.value

        return amount

    def get_inputs_value(self):

        amount = 0

        for input in self.inputs:
            if input.utxo:
                amount += input.utxo.value

        return amount

    # Returns true if new transaction could be created.
    def process_transaction(self, all_utxos: Dict[str, TransactionOutput], minimum_transaction: float):

        if not self.verify_signature():
            print("Transaction signature failed to verify")
            return False

        # gather transaction inputs (make sure they are unspent)
        for inp in self.inputs:
            inp.utxo = all_utxos.get(inp.transaction_output_id)

        inputs_value = self.get_inputs_value()

        if inputs_value < minimum_transaction:
            print("Transaction inputs too small: " + str(inputs_value))
            return False

        if inputs_value < self.value:
            print("Transaction inputs are not sufficient to do transaction")

        self.transaction_id = self.calculate_hash()

        self.outputs.append(TransactionOutput(self.recipient, self.value, self.transaction_id))

        leftover_value = inputs_value - self.value
        if leftover_value > 0:
            self.outputs.append(TransactionOutput(self.sender, leftover_value, self.transaction_id))

        # add outputs to unspent utxos list
        for output in self.outputs:
            all_utxos[output.id] = output

        # remove inputs from utxos list as spent
        for inp in self.inputs:
            if inp.utxo:
                del all_utxos[inp.utxo.id]

        return True

    @classmethod
    def deserialize(cls, info: dict):
        sender = info['sender_public_key']
        receiver = info['receiver_public_key']
        value = info['value']

        inputs = []
        for input_data in info['input']:
            inputs.append(TransactionInput.deserialize(input_data))

        outputs = []
        for output_data in info['output']:
            outputs.append(TransactionOutput.deserialize(output_data))

        transaction = Transaction(sender, receiver, value, inputs)
        transaction.transaction_id = info['id']
        transaction.signature = info['signature']
        transaction.outputs = outputs

        return transaction
