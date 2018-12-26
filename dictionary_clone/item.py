class Item:
    __slots__ = ("key", "value", "hashed_key")

    def __init__(self, key=None, value=None, hashed_key=None):
        self.key = key
        self.value = value
        self.hashed_key = hashed_key
