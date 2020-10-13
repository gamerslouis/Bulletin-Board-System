from .CommandMixin import LoginRequireMixin
from .CommandBase import CommandBase, regist
from models.board import Board, BoardAlreadyExistException
from models.post import Post
from models.user import User
from models.comment import Comment
from models.mail import Mail
from models.ModelBase import ObjectNotExist, ObjectExistMoreThenOne
from core.exception import BadArgsException
from datetime import datetime
import json
from util import gen_uuid


class MailTo(LoginRequireMixin, CommandBase):
    bad_args_message = 'Usage: mail-to <username> --subject <subject> --content <content>'

    def exec(self, *args, **kwargs):
        try:
            username = args[0]
            subject = kwargs['subject']
            content = kwargs['content']
        except (IndexError, KeyError):
            raise BadArgsException

        try:
            user = User.get('username', username)
        except ObjectNotExist:
            self.write('{} does not exist.'.format(username))
            return

        content = content.replace('<br>', '\n')
        uuid = gen_uuid()

        Mail.create(self.user, user, 'mail-{}'.format(uuid), subject)

        self.write(json.dumps({
            'username': username,
            'uuid': 'mail-{}'.format(uuid),
            'subject': subject,
            'content': content
        }))


class ListMail(LoginRequireMixin, CommandBase):
    def exec(self, *args, **kwargs):
        mails = Mail.getmany('receiver_id', self.user.id)
        msg = 'ID\tSubject\tFrom\tDate\n'
        for i, m in enumerate(mails):
            msg += '{}\t{}\t{}\t{}\n'.format(i+1, m.subject, User.get('id', m.sender_id).username,
                                             m.create_date.strftime('%m/%d'))
        self.write(json.dumps({
            'msg': msg
        }))


class RetrMail(LoginRequireMixin, CommandBase):
    bad_args_message = 'Usage: retr-mail <mail#> '

    def exec(self, *args):
        if len(args) != 1:
            raise BadArgsException

        try:
            mail_id = int(args[0])
            assert mail_id > 0
        except Exception:
            raise BadArgsException

        mails = Mail.getmany('receiver_id', self.user.id)

        if len(mails) < mail_id:
            self.write('No such mail.')
            return

        m = mails[mail_id-1]

        self.write(json.dumps({
            'subject': m.subject,
            'from': User.get('id', m.sender_id).username,
            'date': m.create_date.strftime('%Y-%m-%d'),
            'uuid': m.uuid
        }))


class DeleteMail(LoginRequireMixin, CommandBase):
    bad_args_message = 'Usage: delete-mail <mail#>'

    def exec(self, *args):
        if len(args) != 1:
            raise BadArgsException

        try:
            mail_id = int(args[0])
            assert mail_id > 0
        except Exception:
            raise BadArgsException

        mails = Mail.getmany('receiver_id', self.user.id)

        if len(mails) < mail_id:
            self.write('No such mail.')
            return

        mail_uuid = mails[mail_id-1].uuid
        mails[mail_id-1].delete()

        self.write(json.dumps({
            'uuid': mail_uuid
        }))

regist(MailTo, 'mail-to')
regist(ListMail, 'list-mail')
regist(RetrMail, 'retr-mail')
regist(DeleteMail, 'delete-mail')
