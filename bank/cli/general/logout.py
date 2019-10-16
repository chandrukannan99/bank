from cli import BaseCommand
from auth import Auth


class Logout(BaseCommand):
    prefix_list = ('logout',)
    params_template_list = ()

    help = 'Logout user.'

    def run(self):
        Auth.logout_user()

    def show(self, user):
        return bool(user)