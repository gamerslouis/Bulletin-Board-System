from .CommandMixin import LoginRequireMixin
from .CommandBase import CommandBase, regist
from models.board import Board, BoardAlreadyExistException
from models.post import Post
from models.user import User
from models.comment import Comment
from models.ModelBase import ObjectNotExist, ObjectExistMoreThenOne
from core.exception import BadArgsException
from datetime import datetime
from util import gen_uuid
import json


class CreateBoard(LoginRequireMixin, CommandBase):
    bad_args_message = 'Usage: create-board <name>'

    def exec(self, *args):
        try:
            if(len(args) != 1):
                raise BadArgsException
            Board.create(name=args[0], user=self.user)
            self.write('Create board successfully.')
        except BoardAlreadyExistException:
            self.write('Board already exist.')


class CreatePost(LoginRequireMixin, CommandBase):
    bad_args_message = 'Usage: create-post <board-name> --title <title> --content <content>'

    def exec(self, *args, **kwargs):
        try:
            bname = args[0]
            title = kwargs['title']
            content = kwargs['content']
        except (IndexError, KeyError):
            raise BadArgsException

        try:
            board = Board.get('name', bname)
        except ObjectNotExist:
            self.write('Board does not exist.')
            return

        uuid = 'post-{}'.format(gen_uuid())
        content = content.replace('<br>', '\n')

        Post.create(board.id, title, uuid, self.user)
        self.write(json.dumps({
            'uuid': uuid,
            'content': content
        }))


class ListBoard(CommandBase):
    bad_args_message = 'Usage: list-board ##<key>'

    def exec(self, *args):
        if len(args) == 0:
            boards = Board.getall()
        elif len(args) == 1 and len(args[0]) > 2 and args[0][0:2] == '##':
            key = args[0][2:]
            boards = Board.getmany('name', '%{}%'.format(key), True)
        else:
            raise BadArgsException

        msg = 'Index\tName\tModerator\n'

        for i, b in enumerate(boards):
            msg += '{}\t{}\t{}\n'.format(i+1, b.name, User.get(
                'id', b.moderator_id).username)
        self.write(json.dumps({
            'msg': msg
        }))


class ListPost(CommandBase):
    bad_args_message = 'list-post <board-name> ##<key>'

    def exec(self, *args):
        if len(args) in [1, 2]:
            bname = args[0]
        else:
            raise BadArgsException

        key = ''
        if len(args) != 1:
            if len(args[1]) > 2 and args[1][0:2] == '##':
                key = args[1][2:]
            else:
                raise BadArgsException

        try:
            board = Board.get('name', bname)
        except ObjectNotExist:
            self.write('Board does not exist.')
            return

        if key == '':
            posts = Post.getall()
        else:
            posts = Post.getmany('title', '%{}%'.format(key), True)

        posts = filter(lambda p: p.bid == board.id, posts)

        msg = 'ID\tTitle\tAuthor\tDate\n'
        for p in posts:
            msg += '{}\t{}\t{}\t{}\n'.format(p.id, p.title, User.get(
                'id', p.author_id).username, p.create_date.strftime('%m/%d'))

        self.write(json.dumps({
            'msg': msg
        }))


class Read(CommandBase):
    bad_args_message = 'Usage: read <post-id>'

    def exec(self, *args):
        if len(args) != 1:
            raise BadArgsException

        try:
            p = Post.get('id', args[0])
        except ObjectNotExist:
            self.write('Post does not exist.')
            return

        comments = Comment.getmany('post_id', p.id)

        self.write(json.dumps({
            'auther_name': User.get('id', p.author_id).username,
            'title': p.title,
            'date': p.create_date.strftime('%Y-%m-%d'),
            'uuid': p.uuid,
            'comments': [
                {
                    'uuid': c.uuid,
                    'author_name': User.get('id', c.author_id).username
                } for c in comments
            ]
        }))


class DeletePost(LoginRequireMixin, CommandBase):
    bad_args_message = 'Usage: delete-post <post-id>'

    def exec(self, *args):
        if len(args) != 1:
            raise BadArgsException

        try:
            p = Post.get('id', args[0])
        except ObjectNotExist:
            self.write('Post does not exist.')
            return

        if p.author_id != self.user.id:
            self.write('Not the post owner.')
            return

        p.delete()
        comments = Comment.getmany('post_id', p.id)

        self.write(json.dumps({
            'uuid': p.uuid,
            'comments': [c.uuid for c in comments]
        }))


class UpdatePost(LoginRequireMixin, CommandBase):
    bad_args_message = 'Usage: update-post <post-id> --title/content <new>'

    def exec(self, *args, **kwargs):
        if len(args) != 1 or ('title' not in kwargs and 'content' not in kwargs):
            raise BadArgsException

        try:
            p = Post.get('id', args[0])
        except ObjectNotExist:
            self.write('Post does not exist.')
            return

        if p.author_id != self.user.id:
            self.write('Not the post owner.')
            return

        if 'title' in kwargs:
            p.update('title', kwargs['title'])
        if 'content' in kwargs:
            self.write(json.dumps({
                'username': User.get('id', p.author_id).username,
                'uuid': p.uuid,
                'content':  kwargs['content']
            }))
        else:
            self.write('Update successfully.')


class Do_Comment(LoginRequireMixin, CommandBase):
    bad_args_message = 'Usage: comment <post-id> <comment>'

    def exec(self, *args):
        if len(args) < 2:
            raise BadArgsException
        content = self.raw_command.strip()
        content = content[8:].strip()
        content = content[len(args[0]):].strip()

        try:
            p = Post.get('id', args[0])
        except ObjectNotExist:
            self.write('Post does not exist.')
            return

        uuid = 'comment-{}'.format(gen_uuid())
        username = User.get('id', p.author_id).username
        Comment.create(p, self.user, uuid)

        self.write(json.dumps({
            'username': username,
            'uuid': uuid,
            'content': content
        }))


regist(CreateBoard, 'create-board')
regist(CreatePost, 'create-post')
regist(ListBoard, 'list-board')
regist(ListPost, 'list-post')
regist(Read, 'read')
regist(DeletePost, 'delete-post')
regist(UpdatePost, 'update-post')
regist(Do_Comment, 'comment')
