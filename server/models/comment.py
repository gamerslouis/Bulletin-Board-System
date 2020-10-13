from .ModelBase import ModelBase
from core.database import db

class Comment(ModelBase):
    def __init__(self, _id, post_id, author_id, content):
        self.id = _id
        self.post_id = post_id
        self.author_id = author_id
        self.content = content

    @classmethod
    def create(cls,post,user,content):
        db.execute(
            'INSERT INTO comment (post_id, author_id, content) VALUES (?, ?, ?)',
            (post.id, user.id, content))
        db.commit()
