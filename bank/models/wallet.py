import peewee

from blockchain import Wallet as WalletLogic
from blockchain_handler import blockchain_handler
from crypto.aes import AESCipher
from crypto.rsa import new_keys, import_key, one_line_format, pem_format
from models import BaseModel


class Wallet(BaseModel):

    private_key_encrypted = peewee.CharField(max_length=2048)
    public_key_str = peewee.CharField(max_length=512)

    __private_key = None

    def decrypt(self, password):
        cipher = AESCipher(password)

        try:
            private_key_str = cipher.decrypt(self.private_key_encrypted)

            self.__private_key = import_key(pem_format(private_key_str))

        except UnicodeDecodeError:
            raise Exception('Password was invalid to decode private key')

    def get_public_key(self):
        return import_key(pem_format(self.public_key_str))

    def get_private_key(self):
        if not self.__private_key:
            raise Exception("Private key not decrypted")

        return self.__private_key

    def get_private_key_str(self):
        return one_line_format(self.get_private_key().export_key().decode())

    def truncate_keys(self):
        self.public_key = None
        self.__private_key = None

    @staticmethod
    def create_wallet(password):
        wallet = Wallet()
        public_key, private_key = new_keys(1024)
        private_key_as_str = one_line_format(private_key.export_key().decode())
        public_key_str = one_line_format(public_key.export_key().decode())

        cipher = AESCipher(password)
        wallet.private_key_encrypted = cipher.encrypt(private_key_as_str)
        wallet.public_key_str = public_key_str
        wallet.save()

        return wallet

    def get_balance(self):
        wallet = self.get_wallet_logic()
        return wallet.get_balance(blockchain_handler.all_utxos)

    def get_wallet_logic(self):
        w = WalletLogic()
        w.public_key_str = self.public_key_str
        w.private_key = self.__private_key
        return w
