from cli.central_bank import SetFieldCommand


class SetBlockMinerRewardCommand(SetFieldCommand):
    prefix_list = ('set', 'block', 'mining', 'reward')
    field_name = 'block_miner_reward'
    param_key = 'a$'
