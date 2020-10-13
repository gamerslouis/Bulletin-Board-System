from .ModelBase import ModelBase
from core.database import db

class Comment(ModelBase):
    def __init__(self, _id, post_id, author_id, uuid):
        self.id = _id
        self.post_id = post_id
        self.author_id = author_id
        self.uuid = uuid

    @classmethod
    def create(cls,post,user,uuid):
        db.execute(
            'INSERT INTO comment (post_id, author_id, uuid) VALUES (?, ?, ?)',
            (post.id, user.id, uuid))
        db.commit()
