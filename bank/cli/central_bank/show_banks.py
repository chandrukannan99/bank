from cli.central_bank import CentralBankBaseCommand
from models import Bank, Customer


class ShowBanksCommand(CentralBankBaseCommand):

    prefix_list = ('show', 'banks')

    def run(self):
        central_bank = self.get_central_bank()

        print("Total registered banks: %d" % Bank.select().count())
        print()
        print("List of banks")

        index = 1

        print('no\tname\tmanager\tbalance\tcustomer')
        columns_count = 5
        print('-' * (8 * columns_count))

        # TODO: filter by central bank
        for bank in Bank.select():
            customers = Customer.filter(bank=bank)
            balance = bank.manager.wallet.get_balance()

            print('%d\t%s\t%s\t%.2f\t%d' % (index, bank.bank_name, bank.manager.username, balance, len(customers)))
            index += 1

        print()
