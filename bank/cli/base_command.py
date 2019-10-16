

class BaseCommand:
    prefix_list = []
    help = ''
    params_template_list = []

    def run(self, *args):
        if len(args) != len(self.get_params_template_list()):
            raise ValidationError('params length mismatch')

    def has_prefix(self, parts: list):
        if len(self.prefix_list) > len(parts):
            return -1

        for i in range(len(self.prefix_list)):
            if self.prefix_list[i].lower() != parts[i].lower():
                return -1

        return len(self.prefix_list)

    def get_prefix(self):
        return ' '.join(self.prefix_list)

    def get_params_help_text(self):
        return ' '.join(['(%s)' % param for param in self.get_params_template_list()])

    def get_help(self):
        return self.help

    def get_description(self):
        message = self.get_prefix()
        params = self.get_params_help_text()

        if params:
            message += ' ' + params

        help_message = self.get_help()

        if help_message:
            message += ': ' + help_message

        return message

    def show(self, user):
        return True

    def validate_params(self, params):
        if len(params) != len(self.get_params_template_list()):
            raise ValidationError(
                'This command takes %d params, but you provided %d' % (len(self.get_params_template_list()), len(params))
            )

    def get_params_template_list(self):
        return self.params_template_list

    def update_commands(self):
        from cli import command_provider
        from auth import Auth

        command_provider.update(Auth.get_user())


class ValidationError(Exception):
    pass
