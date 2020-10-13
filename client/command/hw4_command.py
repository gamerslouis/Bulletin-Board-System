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
        parsed = {}
        for t in ['author', 'board']:
            parsed[t] = []
        for r in subs:
            parsed[r['type']].append(r)
        for t in ['author', 'board']:
            if len(parsed[t]) == 0:
                continue
            names = list(set([r['name'] for r in parsed[t]]))
            names.sort()
            print('{}: '.format(t.capitalize()), end='')
            for idx, name in enumerate(names):
                print('{}: '.format(name), end='')
                fl = list(filter(lambda i: i['name'] == name, parsed[t]))
                for idx2, r in enumerate(fl):
                    if idx2 != len(fl)-1:
                        print('{}, '.format(r['keyword']), end='')
                    else:
                        print(r['keyword'], end='')
                if idx != len(names)-1:
                    print('; ', end='')
                else:
                    print('')

        # for sub in subs:
        #     print('{}: {}: {}'.format(sub['type'], sub['name'], sub['keyword']))


class Debug(CommandBase):
    def _exec(self, raw, *args, **kwargs):
        code.interact(local=locals())


register(Subscribe, 'subscribe')
register(Unsubscribe)
register(ListSub, 'list-sub')
register(Debug)
