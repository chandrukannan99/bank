from cli.central_bank import CentralBankBaseCommand
from blockchain_handler import blockchain_handler


class ShowBlockchainCommand(CentralBankBaseCommand):

    prefix_list = ('show', 'blockchain')

    def run(self):
        blockchain_handler.blockchain.print()
