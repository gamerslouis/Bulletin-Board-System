from .commandBase import CommandBase, register
from .commandMixin import JsonOrPrintOutMixin, S3Mixin


class MailTO(S3Mixin, JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        self.s3.create_object(
            res['username'],
            res['uuid'],
            {
                'subject': res['subject'],
                'content': res['content']
            }
        )
        print('Sent successfully.')


class ListMail(JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        print(res['msg'])


class RetrMail(S3Mixin, JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        file = self.s3.get_object(self.username, res['uuid'])
        print('Subject\t:{}'.format(res['subject']))
        print('From\t:{}'.format(res['from']))
        print('Date\t:{}'.format(res['date']))
        print('--')
        print(file['content'])


class DeleteMail(S3Mixin, JsonOrPrintOutMixin, CommandBase):
    def handleResponse(self, res, *args, **kwargs):
        self.s3.delete_object(self.username, res['uuid'])
        print('Mail deleted.')


register(MailTO, 'mail-to')
register(ListMail, 'list-mail')
register(RetrMail, 'retr-mail')
register(DeleteMail, 'delete-mail')
