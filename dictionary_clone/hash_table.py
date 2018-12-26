from item import Item


class HashTable:
    def __init__(self):
        self.used = 0
        self.min_size = 10
        self.buckets_record = []
        [self.buckets_record.append(Item()) for i in range(self.min_size)]

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __getitem__(self, key):
        bucket = self.fetch_bucket(key)
        return bucket.value if bucket else None

    def hash_function(self, key):
        return key % len(self.buckets_record)

    def insert(self, key, value):
        hashed_key = self.hash_function(hash(key))
        hashed_bucket = self.buckets_record[hashed_key]

        if hashed_bucket.key:
            if hashed_bucket.key == key and hashed_bucket.hashed_key == hashed_key:
                self.update_bucket(key, value, hashed_bucket)
                print(f"{key} key is updated!")
            else:
                next_hashed_key = self.hash_function(hashed_key + 1)
                next_hashed_bucket = self.buckets_record[next_hashed_key]
                while next_hashed_bucket.key != key and next_hashed_bucket.hashed_key != next_hashed_key:
                    next_hashed_key = self.hash_function(next_hashed_key + 1)
                    next_hashed_bucket = self.buckets_record[next_hashed_key]
                next_hashed_bucket.hashed_key = next_hashed_key
                next_hashed_bucket.key = key
                next_hashed_bucket.value = value
                self.used += 1
        else:
            hashed_bucket.key = key
            hashed_bucket.value = value
            hashed_bucket.hashed_key = hashed_key
            self.used += 1

        if self.used == (self.min_size - 1):
            self.extend_buckets()

    def fetch_bucket(self, key):
        result = None
        hashed_key = self.hash_function(hash(key))
        for bucket in self.buckets_record:
            if bucket.hashed_key == hashed_key and bucket.key == key:
                result = bucket
        return result

    def extend_buckets(self):
        [self.buckets_record.append(Item()) for i in range(self.min_size)]
        self.min_size = self.min_size * 2

    def clear_hash_table(self):
        self.buckets_record = []
        [self.buckets_record.append(Item()) for i in range(self.min_size)]
        self.used = 0
        return self

    def remove_last_index(self):
        buckets = [bucket for bucket in self.buckets_record if bucket.key is not None]
        if buckets and self.used:
            self.clear_bucket(buckets[self.used - 1])

    def clear_bucket(self, key):
        bucket = self.fetch_bucket(key)
        if bucket:
            bucket.key = None
            bucket.value = None
            bucket.hashed_key = None
            self.used -= 1

    def all_items(self):
        return [hashed_item for hashed_item in self.buckets_record if hashed_item.value is not None]

    def update_bucket(self, key, value, bucket):
        bucket.hashed_key = bucket.hashed_key
        bucket.key = key
        bucket.value = value
