import json
import hashlib


class JsonOrPrintOutMixin(object):
    def exec(self, *args, **kwargs):
        res = self.send(self.raw_command)
        try:
            j = json.loads(res)
        except Exception:
            print(res)
            return

        return self.handleResponse(j, *args, **kwargs)


class __S3__(object):
    def __init__(self, s3):
        self.s3 = s3

    def get_user_hash_id(self, username):
        md5 = hashlib.md5()
        md5.update(username.encode())
        return 'user-{}'.format(md5.hexdigest())

    def create_bucket(self, username):
        uuid = self.get_user_hash_id(username)
        self.s3.create_bucket(Bucket=uuid)

    def create_object(self, username: str, file_name: str, content_dict: dict):
        self.s3.Object(
            self.get_user_hash_id(username),
            file_name
        ).put(Body=json.dumps(content_dict))

    def get_object(self, username: str, file_name: str) -> dict:
        content = self.s3.Bucket(self.get_user_hash_id(username)).Object(
            file_name).get()['Body'].read().decode()
        return json.loads(content)

    def delete_object(self, username: str, file_name: str):
        self.s3.Bucket(self.get_user_hash_id(username)).Object(file_name).delete()


class S3Mixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3 = __S3__(self.context['s3'])
