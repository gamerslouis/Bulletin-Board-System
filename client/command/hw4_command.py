from .commandBase import CommandBase, register
from .commandMixin import JsonOrPrintOutMixin
import json
import code


class Subscribe(CommandBase):
    def exec(self, *args, **kwargs):
        response = self.send(self.raw_command)
        if response != 'Subscribe successfully':
            print(response)
            return

        res = self.send('list-sub')
        subs = json.loads(res)['subs']
        self.context['sub_c'].rlock.acquire()
        self.context['sub_c'].subs = subs
        self.context['sub_c'].rlock.release()
        print(response)


class Unsubscribe(CommandBase):
    def exec(self, *args, **kwargs):
        response = self.send(self.raw_command)
        if response != 'Unsubscribe successfully':
            print(response)
            return

        res = self.send('list-sub')
        subs = json.loads(res)['subs']
        self.context['sub_c'].rlock.acquire()
        self.context['sub_c'].subs = subs
        self.context['sub_c'].rlock.release()
        print(response)


class ListSub(JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        subs = res['subs']
        for sub in subs:
            print('{}: {}: {}'.format(sub['type'], sub['name'], sub['keyword']))


class Debug(CommandBase):
    def _exec(self, raw, *args, **kwargs):
        code.interact(local=locals())


register(Subscribe)
register(Unsubscribe)
register(ListSub, 'list-sub')
register(Debug)