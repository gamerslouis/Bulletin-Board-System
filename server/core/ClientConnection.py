import threading
from core.database import close_db
from core.exception import CloseConnect
from command import commands

welcome_message = '********************************\n' + \
                  '** Welcome to the BBS server. **\n' + \
                  '********************************\n'
command_prev = '% '


class ClientConnection(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.daemon = True
        self.conn = conn
        self.addr = addr
        self.message_buffer = b''
        self.context = {}
        self.disconnected = False

    def setup(self):
        self.context = {
            'write_func': self.write,
            'user': None,
        }

    def run(self):
        self.setup()
        print("New connection.")
        try:
            self.conn.sendall(welcome_message.encode())
            while not self.disconnected:
                try:
                    self.conn.sendall(command_prev.encode())
                    command = self.getCommandLine()
                    if command:
                        self.exec(command)
                except CloseConnect:
                    self.disconnected = True
        except Exception as e:
            # print("Unexcept connection error.")
            raise Exception(e)

        # print("One connection disconnected.")
        close_db()
        self.conn.close()
        self.disconnected = True

    def write(self, data, end='\n'):
        self.conn.sendall((data + end).encode())

    def getCommandLine(self):
        while True:
            try:
                message = self.conn.recv(2048)
            except OSError:
                return ''
            if len(message) == 0:
                self.disconnected = True
                return ''
            self.message_buffer += message
            self.message_buffer = self.message_buffer.replace(b'\r\n', b'\n')
            try:
                idx = self.message_buffer.index(b'\n')
                if idx != -1:
                    command = self.message_buffer[:idx]
                    self.message_buffer = self.message_buffer[idx + 1:]
                    return command.decode()
            except ValueError:
                # command line still not end
                pass

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

    def exec(self, command):
        real_com, args, kwargs = self.parse(command)
        if not real_com in commands:
            self.context['write_func']('Command not support')
            return
        commands[real_com](context=self.context)._exec(
            command, *args, **kwargs)

    def stop(self):
        self.disconnected = True
        self.conn.close()
