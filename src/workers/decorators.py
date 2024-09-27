def user_permissions(func):
    def wrapped(self, *args, **kwargs):
        if kwargs.get('user_id') and self.user.id == kwargs.get('user_id') or self.user.is_admin:
            return func(self, *args, **kwargs)
        else:
            return {'error': True, 'msg': 'User don\'t have permissions user'}

    return wrapped


def is_admin(func):
    def wrapped(self, *args, **kwargs):
        if self.user.is_admin:
            return func(self, *args, **kwargs)
        else:
            return {'error': True, 'msg': 'User don\'t have permissions'}

    return wrapped
