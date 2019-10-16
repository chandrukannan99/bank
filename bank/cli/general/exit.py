from cli import BaseCommand


class Exit(BaseCommand):
    prefix_list = ['exit']
    help = 'Exit the Virtual Bank program.'

    def __init__(self):
        self.exit = False

    def run(self, *args):
        self.exit = True
