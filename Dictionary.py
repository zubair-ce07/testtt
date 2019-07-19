"""
Implementation notes:
Traditionally hashmaps are stored sparsely.
For example,
colors = {'ali':'green', 'roma':red', 'umar':'blue'} will be stored as:

    entries = [['--', '--', '--'],
               [127447073495, 'ali', 'green'],
               ['--', '--', '--'],
               ['--', '--', '--'],
               ['--', '--', '--'],
               [511155847987, 'roma', 'red'],
               ['--', '--', '--'],
               [542315338377, 'umar', 'blue']]

Lot of space is wasted. This wasted space can be reduced by using an additional
array like this:

    indices =  [None, 1, None, None, None, 0, None, 2]
    entries =  [[511155847987, 'roma', 'red'],
                [127447073495, 'ali', 'green'],
                [542315338377, 'umar', 'blue']]

1 None takes less space than 3 empty strings
"""


class Entry:
    def __init__(self, digest, key, value):
        self.digest = digest
        self.key = key
        self.value = value


class Dictionary:
    """ Data structure that maps keys to values"""

    def __init__(self, size=8):
        """Optionally specify size of empty dictionary"""
        self.size = size
        self.len = 0
        self.indices = [None] * self.size
        self.entries = []

    def mask(self, digest):
        """Returns array index by bit wise modulus"""
        return digest & (self.size - 1)

    def hash(self, key):
        """Returns hashed key and index for a given key"""
        digest = hash(key)
        index = self.mask(digest)
        return digest, index

    def probe(self, index):
        """Finds the next free index"""
        while self.indices[index] != None:
            index = (index + 1) % self.size
        return index

    def search(self, index, key):
        """Performs a linear search for a given key starting from the given index"""
        if self.indices[index] == None:
            raise KeyError("Key:", key)
        for _ in range(len(self.indices)):
            if self.indices[index] == None or self.entries[self.indices[index]].key != key:
                index = (index + 1) % self.size
            else:
                break
        return index

    def resize(self):
        """If 2/3 of dictionary gets occupied, create a larger dictionary and reinsert existing entries"""
        if self.len / self.size > 0.66:
            old_entries = self.entries
            self.entries = []
            self.size = self.size * 2
            self.len = 0
            self.indices = [None] * self.size
            for entry in old_entries:
                updated_index = self.mask(entry.digest)
                self.insert(updated_index, entry)

    def insert(self, index, entry):
        """Inserts entry at given index"""
        index = self.probe(index)
        self.indices[index] = len(self.entries)
        self.entries.append(entry)
        self.len = self.len + 1
    
    def retrieve(self, index):
        """Returns value at the index (Index should not point to None)"""
        entry_index = self.indices[index]
        return self.entries[entry_index].value

    def delete(self, key):
        """Deletes entry for a given key"""
        _, index = self.hash(key)
        index = self.search(index, key)
        entry_index = self.indices[index]
        self.indices[index] = None
        del self.entries[entry_index]
        self.len = self.len - 1

    def __getitem__(self, key):
        _, index = self.hash(key)
        index = self.search(index, key)
        return self.retrieve(index)

    def __delitem__(self, key):
        self.delete(key)

    def __setitem__(self, key, value):
        digest, index = self.hash(key)
        entry = Entry(digest, key, value)
        self.insert(index, entry)
        self.resize()
    
    def __iter__(self):
        for entry in self.entries:
            if entry is not None:
                yield entry.key
