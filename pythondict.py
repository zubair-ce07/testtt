from dictionary_structure import Dictionary


def main():

    dictionary_obj = Dictionary()
    print(dictionary_obj.fromkeys(('key1', 'key2', 'key3'), 0))
    dictionary_obj.clear()
    
    dictionary_obj['year'] = 2018
    dictionary_obj[23] = 'numeric value'
    dictionary_obj['month'] = 'Dec'
    dictionary_obj['day'] = 'Monday'
    dictionary_obj['brand'] = '_Ford'
    dictionary_obj['model'] = '_Mustang'
    dictionary_obj.pop("day")

    update_dict = Dictionary()
    update_dict['year'] = 2019
    update_dict['color'] = '_White'

    dictionary_obj.update(update_dict)
    dictionary_obj.popitem()
    dictionary_obj.setdefault('DOB', '1993')

    dictionary_obj_copy = dictionary_obj.copy()
    print(dictionary_obj_copy)


if __name__ == "__main__":
    main()
