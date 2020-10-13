from .CommandBase import CommandBase, regist
from models.user import User, UsernameAlreadyExistException, LoginFailException
from core.exception import CloseConnect


class register(CommandBase):
    bad_args_message = 'Usage: register <username> <email> <password>'

    def exec(self, *args):
        try:
            User.register(*args)
            self.write('Register successfully.')
        except UsernameAlreadyExistException:
            self.write('Username is already used.')


class login(CommandBase):
    bad_args_message = 'Usage: login <username> <password>'

    def exec(self, *args):
        if self.user is not None:
            self.write('Please logout first.')
            return
        try:
            self.user = User.login(*args)
            self.write('Welcome, {}.'.format(self.user.username))
        except LoginFailException:
            self.write('Login failed.')


class logout(CommandBase):
    def exec(self, *args):
        if self.user is None:
            self.write('Please login first.')
        else:
            self.write('Bye, {}.'.format(self.user.username))
            self.user = None


class whoami(CommandBase):
    def exec(self, *args):
        if self.context['user'] is None:
            self.write('Please login first.')
        else:
            self.write('{}'.format(self.user.username))


class Exit(CommandBase):
    def exec(self, *args):
        raise CloseConnect


regist(register)
regist(login)
regist(logout)
regist(whoami)
regist(Exit, 'exit')
