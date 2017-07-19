"""
This file contains 'SparseList', 'Node' and 'DictionaryItem' classes
to implement python dictionary class with all default methods
"""


class Node(object):
    """
    'Node' class stores two attributes one is key to identify node
    and the other is list to store python objects
    """

    def __init__(self, key=None):
        self.key = key
        self.items = list()


class SparseList(list):
    """
    'SparseList' class extends python 'list' class and overrides
    '__setitem__' and '__getitem__' methods in addition to that it also implements
    '__binary_search' method to find the 'key' in O(log(n)) to get or set 'value' in minimum time
    """

    def __setitem__(self, key, value):
        """
        :param key: used as an index for the list for insertion
        :param value: used to be set against specific 'key'
        :return: None
        """
        index, min_index, max_index = self.__binary_search(
            key, 0, len(self) - 1)
        if index <= -1:
            node = Node(key=key)
            node.items.append(value)
            self.insert(max(min_index, max_index), node)
        else:
            super(SparseList, self).__getitem__(index).items.append(value)

    def __getitem__(self, key):
        """
        :param key: used as index to get value against it
        :return: if 'key' exists return 'value' else return None
        """
        index, min_index, max_index = self.__binary_search(key, 0, len(self) - 1)
        if index > -1 and super(SparseList, self).__getitem__(index).key == key:
            return super(SparseList, self).__getitem__(index)
        else:
            return None

    def __binary_search(self, key, min, max):
        """
        :param key: used to find an index against it
        :param min: minimum limit to search for index against the 'key'
        :param max: maximum limit to search for index against the 'key'
        :return: if 'key' exists return index of key, max_index, min_index else return -1, min_index, max_index
        """
        if min <= max:
            mid = (min + max) // 2
            if super(SparseList, self).__getitem__(mid).key == key:
                return mid, min, max
            elif super(SparseList, self).__getitem__(mid).key > key:
                return self.__binary_search(key, min, mid - 1)
            elif super(SparseList, self).__getitem__(mid).key < key:
                return self.__binary_search(key, mid + 1, max)
        else:
            return -1, min, max


class DictionaryItem(object):
    """
    'DictionaryItem' is used to store key value pair
    """

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value


class Dictionary(object):
    """
    'Dictionary' is used to store the list of 'DictionaryItem' class using hashed keys
    """

    def __init__(self):
        self.hash_table = SparseList()
        self.size = 0

    def __list_of_field_values(self, field_name):
        """
        :param field_name: key such as 'key' or 'value' against which the values exists of all nodes exists in 'hash_table'
        :return: list of values against 'field_name' such as 'key' or 'value' of all nodes exists in 'hash_table'
        """
        if self.hash_table:
            values = []
            for node in self.hash_table:
                if node:
                    for item in node.items:
                        values.append(item.__dict__[field_name])
            return values
        else:
            return None

    def values(self):
        """
        :return: list of 'value' exists in class instance 'Dictionary'
        """
        return self.__list_of_field_values('value')

    def keys(self):
        """
        :return: list of 'key' exists in class instance 'Dictionary'
        """
        return self.__list_of_field_values('key')

    def clear(self):
        """
        resetting 'Dictionary' instance by making it empty
        :return: None
        """
        self.size = 0
        del self.hash_table[:]

    def get(self, key, default=None):
        """
        :param key: against which the value is required
        :param default: if key does not exists in the 'Dictionary' instance return 'default'
        :return: if key exists in the 'Dictionary' instance return 'value' else return 'default'
        """
        return self[key] if self.has_key(key) else default

    def copy(self):
        """
        :return: 'self' shallow copy of 'Dictionary' instance
        """
        return self

    def pop(self, key):
        """
        :param key: against which the 'value' is to be returned and removed from the 'Dictionary'
        :return: if key exist return 'value' else return 'None'
        """
        value = self[key]
        try:
            del self[key]
            return value
        except KeyError:
            return None

    def has_key(self, key):
        """
        :param key: to checked if it exists in 'Dictionary' instance
        :return: if key exists return True else return False
        """
        return key in self.keys()

    def set_default(self, key, default=None):
        """
        :param key: against which the value is required
        :param default: if key does not exists then set 'default' against key in the 'Dictionary' instance
        :return: 'value' against key in the 'Dictionary' instance
        """
        if not self.has_key(key):
            self[key] = default
        return self[key]

    def fromkeys(cls, keys_sequence, value=None):
        """
        :param keys_sequence: sequence of keys to form dictionary
        :param value: value to be set against sequence of keys
        :return: new 'Dictionary' instance
        """
        if keys_sequence:
            dictionary = Dictionary()
            for key in keys_sequence:
                dictionary[key] = value
        return dictionary

    def update(self, dictionary):
        """
        :param dictionary: whose key value pair is to be inserted in 'Dictionary' instance
        :return: None
        """
        for key in dictionary.keys():
            self[key] = dictionary[key]

    def items(self):
        """
        :return: (key,value) tuples in 'Dictionary' instance
        """
        if self.hash_table:
            key_value = []
            for node in self.hash_table:
                if node:
                    for item in node.items:
                        if item:
                            key_value.append((item.key, item.value))
            return key_value
        else:
            return None

    def __len__(self):
        """
        :return: size/length of 'Dictionary' instance
        """
        return self.size

    def __setitem__(self, key, value):
        """
        :param key: against which the 'value' to set
        :param value: if 'key' exists update 'value' else set 'value' against key
        :return: None
        """
        hashed_key = hash(key)
        if self.hash_table[hashed_key]:
            for item in self.hash_table[hashed_key].items:
                if item.key == key:
                    item.value = value
        else:
            self.hash_table[hashed_key] = DictionaryItem(key=key, value=value)
            self.size += 1

    def __getitem__(self, key):
        """
        :param key: against which a 'value' is required
        :return: if 'key' exists return 'value' saved against it else return None
        """
        hashed_key = hash(key)
        if self.hash_table[hashed_key]:
            for item in self.hash_table[hashed_key].items:
                if item.key == key:
                    return item.value
            return None

    def __delitem__(self, key):
        """
        :param key: entry to be deleted from 'Dictionary' instance
        :return: if key exists return None else raise 'KeyError'
        """
        hashed_key = hash(key)
        if self.hash_table[hashed_key]:
            for item in self.hash_table[hashed_key].items:
                if item.key == key:
                    self.hash_table[hashed_key].items.remove(item)
                    self.size -= 1
                    return
            raise KeyError("no such key: {}".format(key))
        else:
            raise KeyError("no such key: {}".format(key))

    def __contains__(self, item):
        """
        :param item: 'DictionaryItem' to be checked in 'Dictionary' instance
        :return: if item exists return True else return False
        """
        retrieved_item = self.__getitem__(item.key)
        if retrieved_item and retrieved_item.value == item.value:
            return True
        return False

    def __eq__(self, other):
        """
        :param other: another dictionary to be checked if it is the reference of 'Dictionary' instance
        :return: if another dictionary is the same instance of 'Dictionary' return True else return False
        """
        return self.hash_table == other.hash_table

    def __ne__(self, other):
        """
        :param other: another dictionary to be checked if it is the reference of 'Dictionary' instance
        :return: if another dictionary is the same instance of 'Dictionary' return False else return True
        """
        return not self.__eq__(other)

    def __repr__(self):
        """
        :return: printable string of 'Dictionary' instance
        """
        data = list()
        if self.hash_table:
            for node in self.hash_table:
                if node:
                    for item in node.items:
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
        """
        :return: printable string of 'Dictionary' instance
        """
        return self.__repr__()
