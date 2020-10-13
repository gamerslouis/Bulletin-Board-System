class LoginRequireMixin(object):
    def _exec(self, raw_command, *args, **kwargs):
        if self.user is None:
            self.write('Please login first.')
            return
        return super()._exec(raw_command, *args, **kwargs)
