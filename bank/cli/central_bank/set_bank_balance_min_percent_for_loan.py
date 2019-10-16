from cli.central_bank import SetFieldCommand


class SetBankBalanceMinPercentForLoanCommand(SetFieldCommand):
    prefix_list = ('set', 'bank', 'balance', 'percent', 'for', 'loan')

    field_name = 'bank_balance_min_percent_for_loan'
    param_key = '%s'
