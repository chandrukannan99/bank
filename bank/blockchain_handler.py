import json
import os
from shutil import copyfile

from blockchain import BlockChain, Block, Wallet


class BlockchainHandler:

    BLOCKCHAIN_PATH = 'resources/blockchain.json'

    def __init__(self):
        self.blockchain = None
        self.central_bank = None
        self.current_block = None
        self.all_utxos = {}

    def import_json(self, path):
        if os.path.exists(self.BLOCKCHAIN_PATH):
            raise Exception("blockchain file imported previously, if you want to reload it first reset blockchain")

        copyfile(path, self.BLOCKCHAIN_PATH)

        self.load_blockchain()

    def reset_blockchain(self):
        os.remove(self.BLOCKCHAIN_PATH)

        self.load_blockchain()

    def load_blockchain(self):
        from models import CentralBank

        try:
            with open(self.BLOCKCHAIN_PATH) as f:
                blocks_data = json.loads(f.read())

                if not (isinstance(blocks_data, dict) or isinstance(blocks_data, list)):
                    raise Exception("blockchain.json file is not valid")

                if isinstance(blocks_data, dict):
                    blocks_data = [blocks_data]

            self.blockchain = 'pending'
            self.central_bank = CentralBank.get_central_bank()
            if not self.central_bank.has_valid_configuration():
                raise Exception('central bank configuration is not properly set')

            self.blockchain = BlockChain(self.central_bank.difficulty)

            self.all_utxos = {}

            for block_data in blocks_data:
                block = Block.deserialize(block_data)
                self.blockchain.append_block(block, mine_block=False)

                for transaction in block.transactions:

                    for inp in transaction.inputs:
                        del self.all_utxos[inp.transaction_output_id]

                    for output in transaction.outputs:
                        self.all_utxos[output.id] = output

        except Exception as exp:
            print("Error occurred while loading blockchain")
            print(exp)

            self.blockchain = None
            return

        self.blockchain.print()

    def is_blockchain_imported(self):
        return bool(self.blockchain)

    def new_transaction(self, sender_wallet: Wallet, receiver_wallet: Wallet, amount):

        if not self.current_block:
            self.current_block = Block(self.blockchain.last_block_hash())

        transaction = sender_wallet.send_funds(self.all_utxos, receiver_wallet.public_key_str, amount)
        self.current_block.add_transaction(transaction, self.all_utxos, 0.001)

        if len(self.current_block.transactions) == self.central_bank.number_of_transactions_in_block:
            self.blockchain.append_block(self.current_block, True)
            self.current_block = None


blockchain_handler = BlockchainHandler()
