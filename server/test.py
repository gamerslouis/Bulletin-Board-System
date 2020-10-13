
from telnetlib import Telnet
import unittest
import datetime
import os
import sqlite3
import time
from multiprocessing import Process

# setup
port = 7890

update_db = True  # 刪除並重建 db
sql_file = 'db.sqlite'
create_sql_stript = 'createdb.sql'

auto_start_server = True  # 自行啟動server
runserver_file = 'runserver.py'


def runserver():
    os.execvp('python3', ('python3', runserver_file, str(port)))


class TestBase(unittest.TestCase):
    def setUp(self):
        if update_db:
            try:
                os.remove(sql_file)
            except FileNotFoundError:
                pass
            conn = sqlite3.connect(sql_file)
            with open(create_sql_stript, 'r') as f:
                conn.executescript(f.read())

        if auto_start_server:
            self.server_p = Process(target=runserver)
            self.server_p.start()
            time.sleep(0.5)
        self.tn = Telnet("127.0.0.1", 7890)

    def tearDown(self):
        self.tn.write(b'exit\n')
        print('----------------------------------------------------------------------')
        if auto_start_server:
            self.server_p.terminate()
        self.tn.close()

    def command_test(self, command, result):
        self.tn.write(command+b'\n')
        res = self.tn.read_until(b'\n', 1)
        self.assertEqual(res, b'% '+result+b'\n')


class HW1_test(TestBase):
    def test_spec(self):
        self.assertEqual(self.tn.read_until(
            b'\n'), b'********************************\n')
        self.assertEqual(self.tn.read_until(
            b'\n'), b'** Welcome to the BBS server. **\n')
        self.assertEqual(self.tn.read_until(
            b'\n'), b'********************************\n')
        self.command_test(b'register', b'Usage: register <username> <email> <password>')
        self.command_test(b'register Bob bob@qwer.asdf 123456', b'Register successfully.')
        self.command_test(b'register Bob asdf@asdf.asdf 123456', b'Username is already used.')
        self.command_test(b'login', b'Usage: login <username> <password>')
        self.command_test(b'login Bob', b'Usage: login <username> <password>')
        self.command_test(b'login Bob 654321', b'Login failed.')
        self.command_test(b'login Tom 654321', b'Login failed.')
        self.command_test(b'login Bob 123456', b'Welcome, Bob.')
        self.command_test(b'login Bob 123456', b'Please logout first.')
        self.command_test(b'whoami', b'Bob')
        self.command_test(b'logout', b'Bye, Bob.')
        self.command_test(b'logout', b'Please login first.')
        self.command_test(b'whoami', b'Please login first.')


class HW2_test(TestBase):
    def setUp(self):
        super().setUp()
        self.date_str = datetime.datetime.now().strftime('%m/%d')
        self.yeardate_str = datetime.datetime.now().strftime('%Y-%m-%d')

    def test_spec(self):
        self.assertEqual(self.tn.read_until(
            b'\n'), b'********************************\n')
        self.assertEqual(self.tn.read_until(
            b'\n'), b'** Welcome to the BBS server. **\n')
        self.assertEqual(self.tn.read_until(
            b'\n'), b'********************************\n')
        self.command_test(b'create-board NP_HW', b'Please login first.')
        self.command_test(b'register Bob bob@qwer.asdf 123456', b'Register successfully.')
        self.command_test(b'register Sam sam@qwer.com 654321', b'Register successfully.')
        self.command_test(b'login Bob 123456', b'Welcome, Bob.')
        self.command_test(b'create-board NP_HW', b'Create board successfully.')
        self.command_test(b'create-board NP_HW', b'Board already exist.')
        self.command_test(b'create-board OS_HW', b'Create board successfully.')
        self.command_test(b'create-board FF', b'Create board successfully.')

        self.command_test(b'list-board', b'Index\tName\tModerator')
        self.assertEqual(self.tn.read_until(b'\n'), b'1\tNP_HW\tBob\n', 'test list-board')
        self.assertEqual(self.tn.read_until(b'\n'), b'2\tOS_HW\tBob\n', 'test list-board')
        self.assertEqual(self.tn.read_until(b'\n'), b'3\tFF\tBob\n', 'test list-board')

        self.command_test(b'list-board ##HW', b'Index\tName\tModerator')
        self.assertEqual(self.tn.read_until(b'\n'), b'1\tNP_HW\tBob\n', 'test list-board ##HW')
        self.assertEqual(self.tn.read_until(b'\n'), b'2\tOS_HW\tBob\n', 'test list-board ##HW')

        self.command_test(b'create-post NCTU --title About NP HW_2 --content Help!<br>I have some problem!', b'Board does not exist.')
        self.command_test(b'create-post NP_HW --title About NP HW_2 --content Help!<br>I have some problem!', b'Create post successfully.')
        self.command_test(b'create-post NP_HW --title HW_3 --content Ask!<br>Is NP HW_3 Released?', b'Create post successfully.')
        self.command_test(b'list-post NP', b'Board does not exist.')

        self.command_test(b'list-post NP_HW', b'ID\tTitle\tAuthor\tDate')
        self.assertEqual(self.tn.read_until(b'\n'), '1\tAbout NP HW_2\tBob\t{}\n'.format(self.date_str).encode(), 'test list-post NP_HW')
        self.assertEqual(self.tn.read_until(b'\n'), '2\tHW_3\tBob\t{}\n'.format(self.date_str).encode(), 'test list-post NP_HW')

        self.command_test(b'list-post NP_HW ##HW_2', b'ID\tTitle\tAuthor\tDate')
        self.assertEqual(self.tn.read_until(b'\n'), '1\tAbout NP HW_2\tBob\t{}\n'.format(self.date_str).encode(), 'test list-post NP_HW ##HW_2')

        self.command_test(b'read 888', b'Post does not exist.')

        self.command_test(b'read 1', b'Author\t:Bob')
        self.assertEqual(self.tn.read_until(b'\n'), b'Title\t:About NP HW_2\n')
        self.assertEqual(self.tn.read_until(b'\n'), 'Date\t:{}\n'.format(self.yeardate_str).encode())
        self.assertEqual(self.tn.read_until(b'\n'), b'--\n')
        self.assertEqual(self.tn.read_until(b'\n'), b'Help!\n')
        self.assertEqual(self.tn.read_until(b'\n'), b'I have some problem!\n')
        self.assertEqual(self.tn.read_until(b'\n'), b'--\n')

        self.command_test(b'update-post 888 --title NP HW_2', b'Post does not exist.')
        self.command_test(b'update-post 1 --title NP HW_2', b'Update successfully.')

        self.command_test(b'read 1', b'Author\t:Bob')
        self.assertEqual(self.tn.read_until(b'\n'), b'Title\t:NP HW_2\n')
        self.assertEqual(self.tn.read_until(b'\n'), 'Date\t:{}\n'.format(self.yeardate_str).encode())
        self.assertEqual(self.tn.read_until(b'\n'), b'--\n')
        self.assertEqual(self.tn.read_until(b'\n'), b'Help!\n')
        self.assertEqual(self.tn.read_until(b'\n'), b'I have some problem!\n')
        self.assertEqual(self.tn.read_until(b'\n'), b'--\n')

        self.command_test(b'logout', b'Bye, Bob.')
        self.command_test(b'login Sam 654321', b'Welcome, Sam.')
        self.command_test(b'update-post 1 --content Ha!<br>ha!<br>ha!', b'Not the post owner.')
        self.command_test(b'delete-post 1', b'Not the post owner.')
        self.command_test(b'comment 888 Ha! ha! ha!', b'Post does not exist.')
        self.command_test(b'comment 1 Ha! ha! ha!', b'Comment successfully.')

        self.command_test(b'read 1', b'Author\t:Bob')
        self.assertEqual(self.tn.read_until(b'\n'), b'Title\t:NP HW_2\n')
        self.assertEqual(self.tn.read_until(b'\n'), 'Date\t:{}\n'.format(self.yeardate_str).encode())
        self.assertEqual(self.tn.read_until(b'\n'), b'--\n')
        self.assertEqual(self.tn.read_until(b'\n'), b'Help!\n')
        self.assertEqual(self.tn.read_until(b'\n'), b'I have some problem!\n')
        self.assertEqual(self.tn.read_until(b'\n'), b'--\n')
        self.assertEqual(self.tn.read_until(b'\n'), b'Sam: Ha! ha! ha!\n')

        self.command_test(b'create-board Hello', b'Create board successfully.')

        self.command_test(b'list-board', b'Index\tName\tModerator')
        self.assertEqual(self.tn.read_until(b'\n'), b'1\tNP_HW\tBob\n', 'test list-board')
        self.assertEqual(self.tn.read_until(b'\n'), b'2\tOS_HW\tBob\n', 'test list-board')
        self.assertEqual(self.tn.read_until(b'\n'), b'3\tFF\tBob\n', 'test list-board')
        self.assertEqual(self.tn.read_until(b'\n'), b'4\tHello\tSam\n', 'test list-board')

        self.command_test(b'logout', b'Bye, Sam.')
        self.command_test(b'login Bob 123456', b'Welcome, Bob.')
        self.command_test(b'delete-post 1', b'Delete successfully.')
        self.command_test(b'read 1', b'Post does not exist.')
        self.command_test(b'logout', b'Bye, Bob.')


if __name__ == "__main__":
    unittest.main(verbosity=2)
