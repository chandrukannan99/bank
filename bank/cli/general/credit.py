from cli import BaseCommand


class Credit(BaseCommand):
    prefix_list = ['credit']
    help = 'About us'

    def run(self, *args):
        print(r"""
In the name of God

Virtual Bank Project

    Created with love by `Mostafa Jangali` & `Reza Abbasi`
    Course: Data and Network Security
    Sharif University of Technology, Summer 1397

Please type `help` to see commands.
"""
              )
