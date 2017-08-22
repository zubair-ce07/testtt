from builtins import dict


class dict(dict):
    def update(self, m, **kwargs):
        super(dict, self).update(m, **kwargs)
        return self
