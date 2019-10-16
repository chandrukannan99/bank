from cli import BaseCommand
from auth import Auth


class Login(BaseCommand):
    prefix_list = ('login', )
    params_template_list = ('username', 'password')

    help = 'Login user.'

    def run(self, username, password):
        Auth.login_user(username, password)

    def show(self, user):
        return not bool(user)
