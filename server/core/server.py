import socket
import settings
from core.ClientConnection import ClientConnection



class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self._stop = False
        self.clients = []

    def run(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        # print('Start server on {}:{}'.format(self.host, self.port))
        while not self._stop:
            try:
                conn, addr = self.sock.accept()
                client = ClientConnection(conn, addr)
                self.clients.append(client)
                client.start()
            except OSError:
                pass
        self.sock.close()

    def stop(self):
        self._stop = True
        self.sock.close()
        for client in self.clients:
            if client.disconnected == False:
                client.stop()
