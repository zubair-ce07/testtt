class DataNode:
    def __init__(self, is_multiple):
        self.data = {}
        self.sub_data = []
        self.sub_items = []
        self.is_multiple = is_multiple
        self.data.update({"sub_data": self.sub_data})

    def add_sub_items(self, items):
        for item in items:
            if item.is_multiple:
                self.sub_data.append(item.data)
            else:
                item.sub_data = self.data.get('sub_data') + item.data.get('sub_data')
                item.data.update({"sub_data": item.sub_data})
                self.data.update(item.data)

            self.sub_items.append(item)

    def add_data_items(self, item):
        self.data.update(item)

    def print(self):
        for key_value in reversed(self.data.items()):
            if key_value[0] == 'sub_data':
                self._print(key_value[1])
            else:
                print(key_value[0] + "=" + key_value[1])

    def _print(self, dictionaries):
        for dictionary in dictionaries:
            for key_value in reversed(dictionary.items()):
                if key_value[0] == 'sub_data':
                    explore = key_value[1]
                else:
                    print(key_value[0] + "=" + key_value[1])
            self._print(explore)
