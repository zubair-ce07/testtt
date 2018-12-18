

class DictionaryItem(object):
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"<DictionaryItem: key={self.key} value={self.value}>"


class Dictionary(object):
    def __init__(self):
        self.used = 0
        self.min_size = 10
        self.dictionary_items = []
        for i in range(self.min_size):
            self.dictionary_items.append(DictionaryItem())

    def hash_function(self, hashed_value):
        return hashed_value % len(self.dictionary_items)

    def __getitem__(self, key):
        dict_item = self.get_dict_item(key)
        if dict_item is not None:
            return dict_item.value
        return dict_item

    def __setitem__(self, key, value):
        self.insert_dict_item(key, value)
        if self.used == (self.min_size - 1):
            self.resize()

    def __delitem__(self, key):
        dict_item = self.get_dict_item(key)
        if dict_item is not None:
            dict_item.key = None
            dict_item.value = None
            self.used -= 1

    def __repr__(self):
        return "Dictionary({" + ", ".join([f"{key} : {value}" for key, value in self.items()]) + "})"

    def resize(self):
        for i in range(self.min_size):
            self.dictionary_items.append(DictionaryItem())

        self.min_size = self.min_size * 2

    def insert_dict_item(self, key, value):
        hash_value = self.hash_function(hash(key))
        dict_item = self.dictionary_items[hash_value]

        if dict_item.key is None:
            dict_item.key = key
            dict_item.value = value
            self.used += 1
        else:
            if dict_item.key == key:
                dict_item.value = value
            else:
                next_slot = self.hash_function(hash_value + 1)
                next_dict_item = self.dictionary_items[next_slot]

                while next_dict_item.key is not None and next_dict_item.key != key:
                    next_slot = self.hash_function(next_slot + 1)
                    next_dict_item = self.dictionary_items[next_slot]

                if next_dict_item.key is None:
                    next_dict_item.key = key
                    next_dict_item.value = value
                    self.used += 1
                else:
                    next_dict_item.value = value

    def fromkeys(self, keys, value=0):
        self.clear()
        for key in keys:
            self.dictionary_items.append(DictionaryItem(key, value))
        return self

    def clear(self):
        self.used = 0
        self.dictionary_items = []
        for i in range(self.min_size):
            self.dictionary_items.append(DictionaryItem())
        return self

    def keys(self):
        return [dict_item.key for dict_item in self.dictionary_items if dict_item.value is not None]

    def values(self):
        return [dict_item.value for dict_item in self.dictionary_items if dict_item.value is not None]

    def items(self):
        return [(dict_item.key, dict_item.value) for dict_item in self.dictionary_items if dict_item.value is not None]

    def get(self, key, default=0):
        dict_item = self.get_dict_item(key)
        if dict_item is None:
            return default
        return dict_item.value

    def update(self, records):
        for record in records.items():
            dict_item = self.get_dict_item(record[0])
            if dict_item is None:
                self.insert_dict_item(record[0], record[1])
            else:
                dict_item.value = record[1]

    def pop(self, key):
        dict_item = self.get_dict_item(key)
        if dict_item is not None:
            dict_item.key = None
            dict_item.value = None
            self.used -= 1

    def popitem(self):
        if self.used == 0:
            return 'Dictionary is empty !'

        dict_items = [dict_item for dict_item in self.dictionary_items if dict_item.key is not None]
        dict_items[self.used - 1].key = None
        dict_items[self.used - 1].value = None
        self.used -= 1

    def get_dict_item(self, key):
        hash_value = self.hash_function(hash(key))
        value = None
        end_search = False
        initial_value = hash_value
        dict_item = self.dictionary_items[hash_value]

        while dict_item.key is not None and not end_search:
            if dict_item.key == key:
                value = dict_item
                end_search = True
            else:
                hash_value = self.hash_function(hash_value + 1)
                dict_item = self.dictionary_items[hash_value]
                if hash_value == initial_value:
                    return value

        return value

    def setdefault(self, key, value):
        dict_item = self.get_dict_item(key)
        if dict_item is not None:
            return dict_item.value
        else:
            self.insert_dict_item(key, value)
            self.used += 1
            return value

    def copy(self):
        dup_dict = Dictionary()
        for dict_item in self.items():
            dup_dict[dict_item[0]] = dict_item[1]

        return dup_dict
