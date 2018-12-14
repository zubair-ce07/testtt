SIZE=100


class DictionaryItem(object):
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def __repr__(self):
        return "<DictionaryItem: key={0} value={1}>".format(self.key, self.value)


class DictionaryHash(object):
    def __init__(self):
        self.used = 0
        self.table = []
        for i in range(SIZE):
            self.table.append(DictionaryItem())

    def hash_function(self, key, table_size):
        total_sum = sum([ord(key[pos]) for pos in range(len(key))])
        return total_sum % table_size

    def rehash(self, oldhash, table_size):
        return (oldhash + 1) % table_size

    def __getitem__(self, key):
        hash_value = self.hash_function(key, len(self.table))
        value = None
        end_search = False
        initial_value = hash_value
        while self.table[hash_value].key is not None and not end_search:
            if self.table[hash_value].key == key:
                value = self.table[hash_value].value
                end_search = True
            else:
                hash_value = self.rehash(hash_value, len(self.table))
                if hash_value == initial_value:
                    return value

        return value

    def __setitem__(self, key, value):
        self.insert_dict_item(key, value)

    def __delitem__(self, key):
        dict_item = self.get_dict_item(key)
        if dict_item is not None:
            dict_item.key = None
            dict_item.value = None
            self.used -= 1

    def __repr__(self):
        return "DictionaryHash({" + ", ".join([f"{key} : {value}" for key, value in self.items()]) + "})"

    def insert_dict_item(self, key, value):
        hash_value = self.hash_function(key, len(self.table))
        dict_item = self.table[hash_value]
        if dict_item.key is None:
            dict_item.key = key
            dict_item.value = value
            self.used += 1
        else:
            if dict_item.key == key:
                dict_item.value = value
            else:
                next_slot = self.rehash(hash_value, len(self.table))
                next_dict_item = self.table[next_slot]
                while next_dict_item.key is not None and next_dict_item != key:
                    next_slot = self.rehash(next_slot, len(self.table))
                    next_dict_item = self.table[next_slot]

                if self.table[next_slot].key is None:
                    self.table[next_slot].key = key
                    self.table[next_slot].value = value
                    self.used += 1
                else:
                    self.table[next_slot].value = value

    def get_dict_item(self, key):
        hash_value = self.hash_function(key, len(self.table))
        if self.table[hash_value].key == key:
            return self.table[hash_value]
        return None

    def fromkeys(self, keys, value=0):
        self.clear()
        for key in keys:
            self.table.append(DictionaryItem(key, value))
        return self

    def clear(self):
        self.used = 0
        self.table = []
        for i in range(SIZE):
            self.table.append(DictionaryItem())
        return self

    def keys(self):
        return [dict_item.key for dict_item in self.table if dict_item.value is not None]

    def values(self):
        return [dict_item.value for dict_item in self.table if dict_item.value is not None]

    def items(self):
        return [(dict_item.key, dict_item.value) for dict_item in self.table if dict_item.value is not None]

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

        dict_items = [dict_item for dict_item in self.table if dict_item.key is not None]
        dict_items[self.used - 1].key = None
        dict_items[self.used - 1].value = None
        self.used -= 1

    def setdefault(self, key, value):
        dict_item = self.get_dict_item(key)
        if dict_item is not None:
            return dict_item.value
        else:
            self.insert_dict_item(key, value)
            self.used += 1
            return value

    def copy(self):
        dup_dict = DictionaryHash()
        for dict_item in self.items():
            dup_dict[dict_item[0]] = dict_item[1]

        return dup_dict
