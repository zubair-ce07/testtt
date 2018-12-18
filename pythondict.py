from dictionary_hash_structure import Dictionary


def main():

    hash_dict = Dictionary()
    hash_dict['year'] = 2018
    hash_dict[23] = 'numeric value'
    hash_dict['month'] = 'Dec'
    hash_dict['day'] = 'Monday'
    hash_dict['brand'] = '_Ford'
    hash_dict['brand1'] = '_Ford1'
    hash_dict['brand2'] = '_Ford2'
    hash_dict['brand3'] = '_Ford3'
    hash_dict['brand4'] = '_Ford4'
    hash_dict['brand5'] = '_Ford5'
    hash_dict['brand6'] = '_Ford6'
    hash_dict['model7'] = '_Mustang'

    print(hash_dict.fromkeys(('key1', 'key2', 'key3'), 0))

    hash_dict.pop("day")
    update_dict = Dictionary()
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
