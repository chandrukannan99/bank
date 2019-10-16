from cli import BaseCommand
from models import User, BankToken, Bank, CentralBank
from peewee import IntegrityError


class CreateBank(BaseCommand):

    prefix_list = ('create', 'bank')
    params_template_list = ('username', 'password', 'bank_name', 'token')
    help = 'Creates a bank'

    def run(self, username, password, bank_name, token):

        try:
            bank_token = BankToken.get(token=token)
        except BankToken.DoesNotExist:
            raise Exception("token is not valid")

        if Bank.filter(bank_token=bank_token).exists():
            raise Exception("token is consumed, use a new one!")

        try:
            manager = User.create_user(username, password)

        except IntegrityError as e:
            raise Exception("username is duplicate, please choose another")

        try:
            Bank.create(manager=manager, bank_name=bank_name, bank_token=bank_token)
            print("Welcome to virtual bank world ;)")
        except Exception as e:
            print(e)
            raise Exception('Some problem happened in creating bank')

    def show(self, user):
        central_bank = CentralBank.get_central_bank()
        return not user and central_bank and central_bank.has_valid_configuration()
