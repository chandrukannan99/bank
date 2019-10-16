from blockchain_handler import blockchain_handler
from cli.central_bank import CentralBankBaseCommand


class ResetBlockchain(CentralBankBaseCommand):

    prefix_list = ('reset', 'blockchain')
    help = 'removes blockchain file'

    def run(self, path):
        blockchain_handler.reset_blockchain()
        self.update_commands()

    def show(self, user):
        return super(ResetBlockchain, self).show(user) and blockchain_handler.is_blockchain_imported()
