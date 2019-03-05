import hash_table


class MyDictionary:
    def __init__(self):
        self.buckets = hash_table.HashTable()

    def __setitem__(self, key, value):
        self.buckets[key] = value

    def __getitem__(self, key):
        return self.buckets[key]

    def __repr__(self):
        result = str([f"{bucket.key} : {bucket.value}" for bucket in self.buckets.all_items()])
        return f"{'{'}{result}{'}'}"

    def clear(self):
        self.buckets.clear_hash_table()

    def all_keys(self):
        return [dict_item.key for dict_item in self.buckets.all_items()]

    def all_values(self):
        return [dict_item.value for dict_item in self.buckets.all_items()]

    def all_items(self):
        return [(dict_item.key, dict_item.value) for dict_item in self.buckets.all_items()]

    def popitem(self):
        self.buckets.remove_last_index()
