from cli.central_bank import CentralBankBaseCommand
from models import BankToken


class GenerateTokenCommand(CentralBankBaseCommand):

    prefix_list = ('generate', 'token')

    def run(self):

        central_bank = self.get_central_bank()

        if not central_bank.has_valid_configuration():
            raise Exception('Please complete bank configuration first.')

        bank_token = BankToken.create(central_bank=central_bank)
        print("Token created for creating banks!")
        print(bank_token.token)

        return bank_token.token
