from cli.central_bank import SetFieldCommand


class SetDifficultyCommand(SetFieldCommand):
    prefix_list = ('set', 'difficulty', )
    field_name = 'difficulty'
    param_key = 'd'
