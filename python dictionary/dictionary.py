class SparseList(list):
    def __setitem__(self, index, value):
        missing = index - len(self) + 1
        if missing > 0:
            self.extend([None] * missing)
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        try:
            return list.__getitem__(self, index)
        except IndexError:
            return None


class DictionaryItem(object):
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value


class MyDictionary(object):
    def __init__(self, slots=100000):
        self.hash_list = SparseList()
        self.size = 0
        self.slots = slots

    def _custom_hash(self, key):
        return hash(key) % self.slots

    def _list_of_(self, field_name):
        if self.hash_list:
            values = []
            for hashed_items in self.hash_list:
                if hashed_items:
                    for item in hashed_items:
                        values.append(item.__dict__[field_name])
            return values
        else:
            return None

    def values(self):
        return self._list_of_('value')

    def keys(self):
        return self._list_of_('key')

    def clear(self):
        self.size = 0
        del self.hash_list[:]

    def get(self, key, default=None):
        if self.has_key(key):
            return self[key]
        return default

    def copy(self):
        return self

    def pop(self, key):
        value = self[key]
        try:
            del self[key]
            return value
        except KeyError:
            return None

    def has_key(self, key):
        if key in self.keys():
            return True
        return False

    def set_default(self, key, default=None):
        if not self.has_key(key):
            self[key] = default
        return self[key]

    def fromkeys(cls, seq, value=None):
        if seq:
            dictionary = MyDictionary()
            for key in seq:
                dictionary[key] = value
        return dictionary

    def update(self, another_dictionary):
        for key in another_dictionary.keys():
            self[key] = another_dictionary[key]

    def items(self):
        if self.hash_list:
            key_value = []
            for hashed_items in self.hash_list:
                if hashed_items:
                    for item in hashed_items:
                        if item:
                            key_value.append((item.key, item.value))
            return key_value
        else:
            return None

    def __len__(self):
        return self.size

    def __setitem__(self, key, value):

        hashed_key = self._custom_hash(key)

        if not self.hash_list[hashed_key]:
            self.hash_list[hashed_key] = list()
        if self.hash_list[hashed_key]:
            for item in self.hash_list[hashed_key]:
                if item.key == key:
                    item.value = value
        else:
            self.hash_list[hashed_key].append(
                DictionaryItem(key=key, value=value))
            self.size += 1

    def __getitem__(self, key):
        hashed_key = self._custom_hash(key)
        if self.hash_list[hashed_key]:
            for item in self.hash_list[hashed_key]:
                if item.key == key:
                    return item.value
            return None

    def __delitem__(self, key):
        hashed_key = self._custom_hash(key)
        if self.hash_list[hashed_key]:
            for item in self.hash_list[hashed_key]:
                if item.key == key:
                    self.hash_list[hashed_key].remove(item)
                    self.size -= 1
                    return
            raise KeyError("no such key: {}".format(key))
        else:
            raise KeyError("no such key: {}".format(key))

    def __contains__(self, key):
        self.__getitem__(key)

    def __eq__(self, other):
        return other == self.hash_list

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        data = list()
        if self.hash_list:
            for hashed_items in self.hash_list:
                if hashed_items:
                    for item in hashed_items:
                        if item:
                            if isinstance(item.key, str) and isinstance(item.value, str):
                                data.append("'{key}':'{value}'".format(
                                    key=item.key, value=item.value))
                            elif isinstance(item.key, str) and not isinstance(item.value, str):
                                data.append("'{key}':{value}".format(
                                    key=item.key, value=item.value))
                            elif not isinstance(item.key, str) and isinstance(item.value, str):
                                data.append("{key}:'{value}'".format(
                                    key=item.key, value=item.value))
                            else:
                                data.append("{key}:{value}".format(
                                    key=item.key, value=item.value))
        data = ', '.join(data)
        return '{}{}{}'.format('{', data, '}')

    def __str__(self):
        return self.__repr__()
