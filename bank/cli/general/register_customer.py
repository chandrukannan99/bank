from cli import BaseCommand
from models import User, Bank, Customer, CentralBank
from peewee import IntegrityError


class RegisterCustomer(BaseCommand):

    prefix_list = ('register', 'customer')
    params_template_list = ('username', 'password', 'bank_name')
    help = 'Creates a customer'

    def run(self, username, password, bank_name):

        try:
            bank = Bank.get(bank_name=bank_name)
        except Bank.DoesNotExist:
            raise Exception("no bank exists with this name")

        try:
            user = User.create_user(username, password)

        except IntegrityError as e:
            raise Exception("username is duplicate, please choose another")

        try:
            Customer.create(user=user, bank=bank)
            print("Welcome to virtual bank world ;)")
        except Exception as e:
            print(e)
            raise Exception('Some problem happened in creating customer')

    def show(self, user):
        central_bank = CentralBank.get_central_bank()
        return not user and central_bank and central_bank.has_valid_configuration()
