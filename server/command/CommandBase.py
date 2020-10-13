from core.exception import BadArgsException
commands = {}


class CommandBase(object):
    bad_args_message = 'bad args.'

    def __init__(self, context):
        self.context = context

    def write(self, data, end='\n'):
        return self.context['write_func'](data, end=end)

    @property
    def user(self):
        return self.context['user']

    @user.setter
    def user(self, v):
        self.context['user'] = v

    def _exec(self, raw_command, * args, **kwargs):
        self.raw_command = raw_command
        try:
            return self.exec(*args, **kwargs)
        except BadArgsException:
            self.write(self.bad_args_message)

    def exec(self, *args, **kwargs):
        raise NotImplementedError


def regist(command, name=None):
    if name != None:
        commands[name] = command
    else:
        commands[command.__name__] = command
    return command
