import sys
import os
import signal
from core.server import Server
import sqlite3
import settings

def setup_db():
    if not os.path.isfile(settings.db_name):
        conn = sqlite3.connect(settings.db_name)
        with open('createdb.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
        assert port >= 1 and port <= 65536, 'port number can only between 1 and 65536'
    except (ValueError, IndexError):
        print('Usage: {} [Port]'.format(sys.argv[0]), file=sys.stderr)
        exit(1)
    
    setup_db()

    server = Server('localhost', port)
    signal.signal(signal.SIGINT, lambda signal, frame: server.stop())
    signal.signal(signal.SIGTERM, lambda signal, frame: server.stop())
    server.run()
