from dictionary_hash_structure import DictionaryHash


def main():

    hash_dict = DictionaryHash()
    hash_dict['year'] = 2018
    hash_dict['month'] = 'Dec'
    hash_dict['day'] = 'Monday'
    hash_dict['brand'] = '_Ford'
    hash_dict['model'] = '_Mustang'

    print(hash_dict.fromkeys(('key1', 'key2', 'key3'), 0))

    hash_dict.pop("day")
    update_dict = DictionaryHash()
    update_dict['year'] = 2019
    update_dict['color'] = '_White'
    update_dict['last item'] = 'last item'
    hash_dict.update(update_dict)
    hash_dict.popitem()
    hash_dict.setdefault('DOB', '1993')

    hash_dict_copy = hash_dict.copy()
    print(hash_dict_copy)


if __name__ == "__main__":
    main()
