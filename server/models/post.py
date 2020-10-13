from .ModelBase import ModelBase
from core.database import db


class Post(ModelBase):
    def __init__(self, _id, bid, title, author_id, create_date, content):
        self.id = _id
        self.bid = bid
        self.title = title
        self.author_id = author_id
        self.create_date = create_date
        self.content = content

    @classmethod
    def create(self, bid, title, content, user):
        db.execute(
            'INSERT INTO post (bid, title, author_id,content) VALUES (?, ?, ?, ?)',
            (bid, title, user.id, content))
        db.commit()
