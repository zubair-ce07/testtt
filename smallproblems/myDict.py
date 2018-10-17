class MyDict:
    keys = []
    values = []

    def __init__(self, **keyvaluepairs):
        """

        :param keyvaluepairs:
        """
        self.m = len(keyvaluepairs)
        for key, value in sorted(keyvaluepairs.items()):
            self.insert(key, value)

    def __contains__(self, item):
        """

        :param item:
        :return:
        """
        if not isinstance(item, str) or item == '':
            return False
        index = self.search(item)
        if index != -1:
            return True
        return False

    def insert(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        index = self.findhash(key)
        self.keys.insert(index, key)
        self.values.insert(index, value)

    def search(self, key):
        """

        :param key:
        :return:
        """
        if not self.keys:
            return -1
        index = endpoint = self.findhash(key)
        while self.keys[index] != key:
            index = (index + 1) % self.m
            if index == endpoint or self.keys[index] == '':
                return -1
        return index

    def __getitem__(self, key):
        """

        :param key:
        :return:
        """
        index = self.search(key)
        if index != -1:
            return self.values[index]
        # raise KeyError
        print('KeyError: {} not in myDict object'.format(key))

    def get(self, key, default=None):
        """

        :param key:
        :param default:
        :return:
        """
        index = self.search(key)
        if index != -1:
            return self.values[index]
        return default

    def __setitem__(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        index = self.search(key)
        if index != -1:
            self.values[index] = value
        else:
            self.m = self.m + 1
            self.insert(key, value)

    def setdefault(self, key, default=None):
        """

        :param key:
        :param default:
        :return:
        """
        index = self.search(key)
        if index != -1:
            return self.values[index]
        self.m += 1
        self.insert(key, default)
        return default

    def pop(self, key=''):
        """

        :param key:
        :return:
        """
        index = self.search(key)
        if index != -1:
            self.keys.pop(index)
            self.m = self.m - 1
            return self.values.pop(index)
        return None

    def polynomial(self, S, x, p):
        result = S[-1]
        for i in range(-2, -len(S) - 1, -1):
            # result = result* x+S[i]
            result = self.mod_of_addition(self.mod_of_mul(result, x, p), S[i], p)
        return result

    def mod_of_addition(self, a, b, p):
        return (a % p + b % p) % p

    def mod_of_mul(self, a, b, p):
        return (a % p * b % p) % p

    def findhash(self, s):
        m = self.m
        salt = 17
        p = 111143  # 20988936657440586486151264256610222593863921

        s = reversed(s)
        s = [ord(a) for a in s]

        poly = self.polynomial(s, salt, p)
        hashnumber = (poly % p)
        hashnumber = hashnumber % m
        return hashnumber

