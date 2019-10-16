import models
import peewee
from decouple import config


models_list = [
    models.User, models.Wallet, models.CentralBank, models.BankToken, models.Bank, models.Customer,
]


def main():
    # create database and tables
    for model in models_list:
        model.create_table()

    # create superuser
    try:
        user = models.User.create_user(config('superuser_username'), config('superuser_password'))
        user.is_superuser = True
        user.save()

    except peewee.IntegrityError as e:
        print("Exception: " + str(e))

    test_data()


def test_data():
    from cli import command_provider

    # create central bank manager
    try:
        command_provider.get_command('CreateManager').run('manager', '12345')
    except:
        pass
    command_provider.get_command('Login').run('manager', '12345')

    command_provider.get_command('SetBankBalanceMinPercentForLoanCommand').run(300)
    command_provider.get_command('SetBlockMinerRewardCommand').run(0.1)
    command_provider.get_command('SetDifficultyCommand').run(3)
    command_provider.get_command('SetTransactionFeeCommand').run(0.1)
    command_provider.get_command('SetNumberOfTransactionsInBlockCommand').run(4)

    token = command_provider.get_command('GenerateTokenCommand').run()

    command_provider.get_command('Logout').run()

    command_provider.get_command('CreateBank').run('mellat', '12345', 'Mellat', token)


if __name__ == '__main__':
    main()
