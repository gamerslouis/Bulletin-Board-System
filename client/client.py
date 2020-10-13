from command import commands
# from command import Subscribe


class Client(object):
    def __init__(self, sock, s3):
        self.context = {}
        self.context['sock'] = sock
        self.context['s3'] = s3
        # self.context['sub_p'] = Subscribe.Producer()
        # self.context['sub_c'] = Subscribe.Consumer()

    def exec(self):
        print('********************************')
        print('** Welcome to the BBS server. **')
        print('********************************')

        while True:
            print('% ', end='')
            raw_command = input()
            if raw_command == '':
                continue
            command, args, kwargs = self.parse(raw_command)
            kwargs['raw_command'] = raw_command
            if command == 'exit':
                break
            if command in commands:
                # try:
                commands[command](context=self.context)._exec(raw_command, *args, **kwargs)
                # except Exception:
                #     print('Unaccepted Error!!')
            else:
                print('Command not found')

        self.context['sock'].close()

    def parse(self, command):
        c = command.strip()
        if c == '':
            return '', [], {}
        args = []
        kwargs = {}
        kmode = False
        smode = True
        s = 0
        for i in range(len(c)):
            if smode:
                if c[i] != ' ':
                    smode = False
                    s = i
                    if len(c) > i+1 and c[i:i+2] == '--':
                        kmode = True
                        s = i+2
                else:
                    continue
            if c[i] == ' ':
                if not kmode:
                    args.append(c[s:i])
                    smode = True
                elif len(c) > i+1 and c[i+1:i+3] == '--':
                    k = c[s:].find(' ')
                    if c[s:s+k] != '':
                        kwargs[c[s:s+k]] = c[s+k+1:i]
                    elif c[s+k+1:] != '':
                        kwargs[c[s+k:i]] = ''

                    smode = True
        if kmode:
            k = c[s:].find(' ')
            if c[s:s+k] != '':
                kwargs[c[s:s+k]] = c[s+k+1:]
            elif c[s+k+1:] != '':
                kwargs[c[s+k+1:]] = ''
        else:
            args.append(c[s:])

        if len(args) > 1:
            return args[0], args[1:], kwargs
        else:
            return args[0], [], kwargs
