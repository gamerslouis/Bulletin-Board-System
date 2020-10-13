import hashlib
from core.exception import BadArgsException
from core.database import db
from .ModelBase import ModelBase


class LoginFailException(Exception):
    pass


class WrongPasswordException(LoginFailException):
    pass


class UsernameNotExistException(LoginFailException):
    pass


class UsernameAlreadyExistException(Exception):
    pass


class User(ModelBase):
    def __init__(self, _id, username, email, password):
        self.id = _id
        self.username = username
        self.email = email
        self.password = password

    @classmethod
    def register(cls, *args):
        if len(args) != 3:
            raise BadArgsException
        cur = db.cursor()
        res = cur.execute(
            'select username from user where username = ?', [args[0]])
        if res.fetchone() != None:
            raise UsernameAlreadyExistException

        hashed_pass = cls.sha_pass(args[2])
        cur.execute(
            'INSERT INTO user (username, email, password) VALUES (?, ?, ?)', [*args[0:2], hashed_pass])
        db.commit()

    @classmethod
    def login(cls, *args):
        if len(args) != 2:
            raise BadArgsException
        cur = db.cursor()
        res = cur.execute(
            'select id, username, email, password from user where username = ?', [args[0]])
        res = res.fetchone()
        if res is None:
            raise UsernameNotExistException
        if cls.sha_pass(args[1]) != res[3]:
            raise WrongPasswordException

        return User(*res)

    @classmethod
    def sha_pass(cls, password):
        s = hashlib.sha256()
        s.update(password.encode())
        return s.hexdigest()
