from core.database import db


class ObjectNotExist(Exception):
    pass


class ObjectExistMoreThenOne(Exception):
    pass


class ModelBase(object):
    @classmethod
    def get(cls, key, value, like=False):
        cur = db.cursor()
        cur.execute(
            'select * from {} where {} {} ?'.format(cls.__name__.lower(), key, 'like'if like else '='), (value,))
        res = cur.fetchall()
        if len(res) == 0:
            raise ObjectNotExist
        if len(res) > 1:
            raise objectExistMoreThenOne
        return cls(*res[0])

    @classmethod
    def getmany(cls, key, value, like=False):
        cur = db.cursor()
        cur.execute('select * from {} where {} {} ?'.format(cls.__name__.lower(),
                                                            key, 'like'if like else '='), (value,))
        res = cur.fetchall()
        objs = [cls(*row) for row in res]
        return objs

    @classmethod
    def getall(cls):
        cur = db.cursor()
        cur.execute('select * from {}'.format(cls.__name__.lower()))
        res = cur.fetchall()
        objs = [cls(*row) for row in res]
        return objs

    def delete(self):
        db.execute('delete from {} where id= ?'.format(
            self.__class__.__name__.lower()), (self.id,))

    def update(self, key, value):
        db.execute('update {} set {} = ? where id = {}'.format(
            self.__class__.__name__.lower(), key, self.id), (value,))
        db.commit()