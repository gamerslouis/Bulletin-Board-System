from .ModelBase import ModelBase
from core.database import db
from datetime import datetime


class Post(ModelBase):
    def __init__(self, _id, bid, title, author_id, create_date, uuid):
        self.id = _id
        self.bid = bid
        self.title = title
        self.author_id = author_id
        self.create_date = datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S')
        self.uuid = uuid

    @classmethod
    def create(self, bid, title, uuid, user):
        db.execute(
            'INSERT INTO post (bid, title, author_id,uuid) VALUES (?, ?, ?, ?)',
            (bid, title, user.id, uuid))
        db.commit()
