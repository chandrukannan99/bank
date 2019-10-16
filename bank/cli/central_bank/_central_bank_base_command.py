from cli import BaseCommand
from auth import Auth
from models import CentralBank


class CentralBankBaseCommand(BaseCommand):

    def get_central_bank(self):
        user = Auth.get_user()

        try:
            return CentralBank.get(manager=user)
        except CentralBank.DoesNotExist:
            return None

    def show(self, user):
        return bool(self.get_central_bank())
