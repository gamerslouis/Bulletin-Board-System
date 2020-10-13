from models.subscribe import Subscribe as SubscribeModel, SubscribeJsonEncoder
from .CommandMixin import LoginRequireMixin
from .CommandBase import CommandBase, regist
from core.exception import BadArgsException
from core.database import db
import json


class Subscribe(LoginRequireMixin, CommandBase):
    bad_args_message = 'subscribe --board <board-name>/--author <author-name> --keyword <keyword>'

    def exec(self, *args, **kwargs):
        try:
            keyword = kwargs['keyword']
            board = kwargs.get('board', '')
            author = kwargs.get('author', '')
        except (IndexError, KeyError):
            raise BadArgsException

        if board == '' and author == '':
            raise BadArgsException
        _type = 'board' if board != '' else 'author'
        name = board if board != '' else author

        cur = db.cursor()
        cur.execute('select id from subscribe where owner_id=? and type=? and name=? and keyword=?',
                    (self.user.id, _type, name, keyword))
        if len(cur.fetchall()) > 0:
            self.write('Already subscribed')
            return

        SubscribeModel.create(self.user,
                              _type='board' if board != '' else 'author',
                              name=board if board != '' else author,
                              keyword=keyword
                              )
        self.write('Subscribe successfully')


class Unsubscribe(LoginRequireMixin, CommandBase):
    bad_args_message = 'unsubscribe --board <board-name>/ --author <author-name> '

    def exec(self, *args, **kwargs):
        board = kwargs.get('board', '')
        author = kwargs.get('author', '')
        if board == ''and author == '':
            raise BadArgsException

        _type = 'board' if board != '' else 'author'
        name = board if board != '' else author

        cur = db.cursor()
        cur.execute('select id from subscribe where owner_id=? and type=? and name=?',
                    (self.user.id, _type, name))
        if len(cur.fetchall()) == 0:
            self.write('You haven\'t subscribed {}'.format(name))
            return

        cur.execute('delete from subscribe where owner_id=? and type=? and name=?',
                    (self.user.id, _type, name))
        db.commit()
        self.write('Unsubscribe successfully')


class ListSub(LoginRequireMixin, CommandBase):
    def exec(self, *args, **kwargs):
        subs = SubscribeModel.getmany('owner_id', self.user.id)

        self.write(json.dumps({
            'subs': subs
        }, cls=SubscribeJsonEncoder))


regist(Subscribe, 'subscribe')
regist(Unsubscribe, 'unsubscribe')
regist(ListSub, 'list-sub')
