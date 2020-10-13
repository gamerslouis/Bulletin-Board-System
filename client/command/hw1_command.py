from .commandBase import CommandBase, register
from .commandMixin import S3Mixin
import json


class Register(S3Mixin, CommandBase):
    def exec(self, *args, **kwargs):
        res = self.send(self.raw_command)

        if(res != 'Register successfully.'):
            print(res)
            return

        self.s3.create_bucket(args[0])
        print(res)


class login(S3Mixin, CommandBase):
    def exec(self, *args, **kwargs):
        res = self.send(self.raw_command)

        if(res != 'Welcome.'):
            print(res)
            return

        self.context['user'] = args[0]
        self.context['sub_p'].username = args[0]
        res = self.send('list-sub')
        subs = json.loads(res)['subs']
        self.context['sub_c'].subs = subs
        self.context['sub_c'].run()

        print('Welcome, {}.'.format(args[0]))


class logout(CommandBase):
    def exec(self, *args, **kwargs):
        res = self.send(self.raw_command)

        if not res.startswith('Bye'):
            print(res)
            return
            
        user = self.context['user']
        del self.context['user']
        self.context['sub_c'].stop()

        print('Bye, {}.'.format(user))


class whoami(CommandBase):
    pass


register(Register)
register(login)
register(logout)
register(whoami)
