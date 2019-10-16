import cli


class CommandProvider:

    def __init__(self):
        self.exit_command = cli.general.Exit()
        self.help_command = cli.general.Help(self)
        self.credit_command = cli.general.Credit()

        self.all_commands = [

            # central bank
            cli.central_bank.ShowConfigurationCommand(),
            cli.central_bank.ShowBanksCommand(),
            cli.central_bank.ShowBlockchainCommand(),
            cli.central_bank.GenerateTokenCommand(),
            cli.central_bank.SetNumberOfTransactionsInBlockCommand(),
            cli.central_bank.SetTransactionFeeCommand(),
            cli.central_bank.SetDifficultyCommand(),
            cli.central_bank.SetBlockMinerRewardCommand(),
            cli.central_bank.SetBankBalanceMinPercentForLoanCommand(),
            cli.central_bank.ImportBlockchain(),
            cli.central_bank.ResetBlockchain(),

            # user
            cli.user.GetBalanceCommand(),
            cli.user.TransferMoneyCommand(),
            cli.user.GetPublicKeyCommand(),
            cli.user.GetPrivateKeyCommand(),

            # general
            cli.general.Login(),
            self.help_command,
            cli.general.CreateManager(),
            cli.general.CreateBank(),
            cli.general.RegisterCustomer(),
            cli.general.Logout(),
            self.credit_command,
            self.exit_command,
        ]

        self.commands = None

        self.update(None)

    def get_commands(self):
        return self.commands

    def update(self, user):

        self.commands = []

        for command in self.all_commands:
            if command.show(user):
                self.commands.append(command)

    def get_command(self, class_name):
        for command in self.all_commands:
            if command.__class__.__name__ == class_name:
                return command
