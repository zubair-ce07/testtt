
class DictionaryReplica(object):
    def __init__(self):
        self.my_dict = {}

    def _get(self, key):
        try:
            return self.my_dict[key]
        except KeyError:
            return None

    def _add(self, key, val):
        self.my_dict[key] = val

    def _pop(self, key):
        del self.my_dict[key]

    def _popitem(self):
        keys = [x for x in self.my_dict]
        try:
            del self.my_dict[keys[-1]]
        except KeyError:
            return 'Dictionary is empty !'

    def _setdefault(self, key, val):
        try:
            return self.my_dict[key]
        except KeyError:
            self.my_dict[key] = val
            return self.my_dict[key]

    def _update(self, record):
        for key in record:
            self.my_dict[key] = record[key]

    def _fromkeys(self, keys, val):
        self.my_dict = {}
        for key in keys:
            self.my_dict[key] = val

        return self.my_dict

    def _keys(self):
        return [x for x in self.my_dict]

    def _values(self):
        return {self.my_dict[x] for x in self.my_dict}

    def _clear(self):
        for key in list(self.my_dict):
            try:
                del self.my_dict[key]
            except KeyError:
                return 'Dictionary is clearing failed !'

        return self.my_dict

    def _items(self):
        return {(x, self.my_dict[x]) for x in self.my_dict}

    def _copy(self):
        return {x:self.my_dict[x] for x in self.my_dict}
