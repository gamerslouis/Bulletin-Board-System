from .ModelBase import ModelBase
from core.database import db
from datetime import datetime
import json


class Subscribe(ModelBase):
    def __init__(self, _id, owner_id, _type, name, keyword):
        self.id = _id
        self.owner_id = owner_id
        self.type = _type
        self.name = name
        self.keyword = keyword

    @classmethod
    def create(self, owner, _type, name, keyword):
        db.execute(
            'INSERT INTO subscribe (owner_id, type,name,keyword) VALUES (?, ?, ?, ?)',
            (owner.id, _type, name, keyword))
        db.commit()


class SubscribeJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Subscribe):
            return {
                'owner_id': obj.owner_id,
                'type': obj.type,
                'name': obj.name,
                'keyword': obj.keyword
            }
        return super().default(self, obj)
