from cli import BaseCommand


class UserBaseCommand(BaseCommand):

    def show(self, user):
        return bool(user)
