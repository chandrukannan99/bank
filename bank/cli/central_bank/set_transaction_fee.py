from cli.central_bank import SetFieldCommand


class SetTransactionFeeCommand(SetFieldCommand):
    prefix_list = ('set', 'transaction', 'fee')
    field_name = 'transaction_fee'
    param_key = 'z$'
