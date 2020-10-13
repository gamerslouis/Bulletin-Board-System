from .commandBase import CommandBase, register
from .commandMixin import S3Mixin, JsonOrPrintOutMixin


class CreateBoard(CommandBase):
    pass


class ListBoard(JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        print(res['msg'])


class ListPost(JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        print(res['msg'])


class CreatePost(S3Mixin, JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        self.s3.create_object(self.username, res['uuid'], {'content': res['content']})
        self.context['sub_p'].new_post(args[0], kwargs['title'])
        print('Create post successfully.')


class Read(S3Mixin, JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        print('Author\t:{}'.format(res['auther_name']))
        print('Title\t:{}'.format(res['title']))
        print('Date\t:{}'.format(res['date']))
        print('--')

        p_content = self.s3.get_object(res['auther_name'], res['uuid'])['content']
        print(p_content)
        print('--')

        for c in res['comments']:
            print('{}: {}'.format(c['author_name'], self.s3.get_object(res['auther_name'], c['uuid'])['content']))


class DeletePost(S3Mixin, JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        self.s3.delete_object(self.username, res['uuid'])
        for c in res['comments']:
            self.s3.delete_object(self.username, c)
        print('Delete successfully.')


class UpdatePost(S3Mixin, JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        self.s3.create_object(res['username'], res['uuid'], {'content': res['content']})
        print('Update successfully.')


class Do_Comment(S3Mixin, JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        self.s3.create_object(res['username'], res['uuid'], {'content': res['content']})
        print('Comment successfully.')


register(CreateBoard, 'create-board')
register(CreatePost, 'create-post')
register(ListBoard, 'list-board')
register(ListPost, 'list-post')
register(Read, 'read')
register(DeletePost, 'delete-post')
register(UpdatePost, 'update-post')
register(Do_Comment, 'comment')
