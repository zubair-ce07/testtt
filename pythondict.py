from dictionaryreplica import DictionaryReplica


def main():
    dict_replica = DictionaryReplica()
    print(dict_replica._fromkeys(('key1', 'key2', 'key3'), 0))

    dict_replica._add('brand', '__Ford')
    dict_replica._add('model', '__Mustang')
    dict_replica._add('year', '__year')

    print(dict_replica._copy())
    print(dict_replica._get("model"))
    print(dict_replica._items())
    print(dict_replica._keys())

    dict_replica._pop("model")
    dict_replica._update({'color': '_White'})

    print(dict_replica._values())
    dict_replica._popitem()
    print(dict_replica._values())

if __name__ == "__main__":
    main()
