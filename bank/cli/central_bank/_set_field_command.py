from cli.central_bank import CentralBankBaseCommand
import peewee


class SetFieldCommand(CentralBankBaseCommand):
    field_name = ''
    param_key = ''
    help = ''

    _filed_types = {
        peewee.IntegerField: int,
        peewee.FloatField: float,
        peewee.SmallIntegerField: int,
    }

    def run(self, value):
        central_bank = self.get_central_bank()

        field_type = type(getattr(central_bank, self.field_name))
        field_cleaner = self._filed_types.get(field_type, str)
        value = field_cleaner(value)

        setattr(central_bank, self.field_name, value)

        central_bank.save()

    def get_params_template_list(self):
        return (self.param_key,)