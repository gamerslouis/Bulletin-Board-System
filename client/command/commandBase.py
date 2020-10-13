import hashlib
from util import SendServer
import json

commands = {}


class CommandBase(object):
    def __init__(self, context):
        self.context = context

    @property
    def sock(self):
        return self.context['sock']

    @property
    def username(self):
        return self.context['user']

    def exec(self, *args, **kwargs):
        print(self.send(self.raw_command))

    def send(self, command):
        return SendServer(self.sock, command)

    def _exec(self, raw, *args, **kwargs):
        self.raw_command = raw
        return self.exec(*args, **kwargs)


class Help(CommandBase):
    def exec(self, *args, **kwargs):
        for c in commands.keys():
            print(c)


def register(command, name=None):
    if name != None:
        commands[name] = command
    else:
        commands[command.__name__.lower()] = command
    return command


register(Help)
