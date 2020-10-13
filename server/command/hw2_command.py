from .CommandMixin import LoginRequireMixin
from .CommandBase import CommandBase, regist
from models.board import Board, BoardAlreadyExistException
from models.post import Post
from models.user import User
from models.comment import Comment
from models.ModelBase import ObjectNotExist, ObjectExistMoreThenOne
from core.exception import BadArgsException
from datetime import datetime


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

        content = content.replace('<br>', '\n')

        Post.create(board.id, title, content, self.user)
        self.write('Create post successfully.')


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

        self.write('Index\tName\tModerator')
        for i, b in enumerate(boards):
            self.write('{}\t{}\t{}'.format(i+1, b.name, User.get(
                'id', b.moderator_id).username))


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
        self.write('ID\tTitle\tAuthor\tDate')
        for p in posts:
            date = datetime.strptime(p.create_date, '%Y-%m-%d %H:%M:%S')
            self.write('{}\t{}\t{}\t{}'.format(p.id, p.title, User.get(
                'id', p.author_id).username, date.strftime('%m/%d')))


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

        date = datetime.strptime(p.create_date, '%Y-%m-%d %H:%M:%S')

        self.write('Author\t:{}'.format(User.get('id', p.author_id).username))
        self.write('Title\t:{}'.format(p.title))
        self.write('Date\t:{}'.format(date.strftime('%Y-%m-%d')))
        self.write('--')
        self.write(p.content)
        self.write('--')

        comments = Comment.getmany('post_id', p.id)

        for c in comments:
            self.write('{}: {}'.format(
                User.get('id', c.author_id).username, c.content))


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
        self.write('Delete successfully.')


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
            p.update('content', kwargs['content'])

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

        Comment.create(p, self.user, content)
        self.write('Comment successfully.')

regist(CreateBoard, 'create-board')
regist(CreatePost, 'create-post')
regist(ListBoard, 'list-board')
regist(ListPost, 'list-post')
regist(Read, 'read')
regist(DeletePost, 'delete-post')
regist(UpdatePost, 'update-post')
regist(Do_Comment, 'comment')
regist(ListBoard, 'list-board')
