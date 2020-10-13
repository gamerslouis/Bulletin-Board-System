
from core.database import db
from .ModelBase import ModelBase


class BoardAlreadyExistException(Exception):
    pass


class Board(ModelBase):
    def __init__(self, _id, name, moderator_id):
        self.id = _id
        self.name = name
        self.moderator_id = moderator_id

    @classmethod
    def create(self, name, user):
        cur = db.cursor()
        res = cur.execute(
            'select name from board where name = ?', [name,])
        if res.fetchone() != None:
            raise BoardAlreadyExistException

        cur.execute(
            'INSERT INTO board (name, moderator_id) VALUES (?, ?)', [name, user.id])
        db.commit()
