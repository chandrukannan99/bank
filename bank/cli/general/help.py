from cli import BaseCommand


class Help(BaseCommand):
    prefix_list = ['help']
    help = 'Show the list of commands'

    def __init__(self, command_provider):
        self.command_provider = command_provider

    def run(self, *args):
        print("Commands list")
        for com in self.command_provider.get_commands():
            print('   ' + com.get_description())
