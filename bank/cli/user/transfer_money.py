from auth import Auth
from cli.user import UserBaseCommand
from models import User, Customer
from blockchain_handler import blockchain_handler


class TransferMoneyCommand(UserBaseCommand):

    prefix_list = ('transfer', )
    params_template_list = ('amount', 'receiver_username')

    def run(self, amount, receiver_username):
        sender = Auth.get_user()
        amount = float(amount)

        if amount <= 0:
            raise Exception("Amount should be positive")

        try:
            receiver = User.get(username=receiver_username)
        except User.DoesNotExist:
            raise Exception("Receiver does not exist in system")

        sender_wallet = sender.wallet.get_wallet_logic()
        receiver_wallet = receiver.wallet.get_wallet_logic()

        try:
            customer = Customer.get(user=sender)
            sender_bank_wallet = customer.bank.manager.wallet.get_wallet_logic()
        except Customer.DoesNotExist:
            sender_bank_wallet = None

        if sender_bank_wallet and sender_wallet.get_balance(blockchain_handler.all_utxos) < \
                blockchain_handler.central_bank.transaction_fee + amount:
            raise Exception("sender balance is not sufficient to handle fee")

        blockchain_handler.new_transaction(
            sender_wallet,
            receiver_wallet,
            amount
        )

        if sender_bank_wallet:
            blockchain_handler.new_transaction(
                sender_wallet,
                sender_bank_wallet,
                blockchain_handler.central_bank.transaction_fee
            )
