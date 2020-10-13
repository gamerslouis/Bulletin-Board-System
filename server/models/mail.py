from .ModelBase import ModelBase
from core.database import db
from datetime import datetime


class Mail(ModelBase):
    def __init__(self, _id, receiver_id, sender_id, create_date, uuid, subject):
        self.id = _id
        self.receiver_id = receiver_id
        self.sender_id = sender_id
        self.create_date = datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S')
        self.uuid = uuid
        self.subject = subject

    @classmethod
    def create(cls, sender, receiver, uuid, subject):
        db.execute(
            'INSERT INTO mail (receiver_id, sender_id, uuid, subject) VALUES (?, ?, ?, ?)',
            (receiver.id, sender.id, uuid, subject))
        db.commit()
