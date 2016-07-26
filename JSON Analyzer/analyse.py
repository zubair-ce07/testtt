import json
import argparse

_key_occurence_stats = dict()
_values_of_keys = dict()


def extract_all_keys(given_dictionary, previous_key):
    "Function that extracts all the keys of a dictionary at all levels"
    for each_key in given_dictionary:
        key = previous_key+each_key
        if key in _key_occurence_stats:
            _key_occurence_stats[key] += 1
        else:
            _key_occurence_stats[key] = 1
        if type(given_dictionary[each_key]) is dict:
            extract_all_keys(given_dictionary[each_key], key + '.')
    return


def extract_all_values(given_dictionary, given_key, parent_key, valid_keys, non_valid_keys):
    "Function that extracts all the values of a dictionary at all levels"
    for key in given_dictionary:
        key_heirarchy = parent_key + key
        if (key == given_key and key in valid_keys):
            value_of_key = given_dictionary[key]
            if ((isinstance(value_of_key,list)) and (key not in non_valid_keys)):
                for each_item in value_of_key:
                    key_heirarchy_string = parent_key + key + ':' + each_item
                    if key_heirarchy_string in _values_of_keys:
                        _values_of_keys[key_heirarchy_string] += 1
                    else:
                        _values_of_keys[key_heirarchy_string] = 1
            elif isinstance(value_of_key,dict):
                for each_sub_key in value_of_key:
                    if isinstance(value_of_key[each_sub_key],dict):
                        value_of_subkey = str(each_sub_key)
                        my_parent_key = (key_heirarchy.split('.'))[-1]
                        if (each_sub_key in valid_keys or my_parent_key not in non_valid_keys):
                            valid_keys.append(value_of_subkey)
                            extract_all_values(value_of_key, each_sub_key, key_heirarchy +'.', valid_keys, non_valid_keys)
                    elif type(value_of_key[each_sub_key]) is list:
                        extract_all_values(value_of_key, each_sub_key, key_heirarchy, valid_keys, non_valid_keys)
                    else:
                        top_level_key = (key_heirarchy.split('.'))[-1]
                        if (each_sub_key in valid_keys or top_level_key not in non_valid_keys):
                            top_level_key=key_heirarchy+'.'+each_sub_key+":"+str(value_of_key[each_sub_key])
                            if top_level_key in _values_of_keys:
                                _values_of_keys[top_level_key] += 1
                            else:
                                _values_of_keys[top_level_key] = 1
            elif (key not in non_valid_keys):
                if value_of_key in _values_of_keys:
                    _values_of_keys[value_of_key] += 1
                else:
                    _values_of_keys[value_of_key] = 1
    return


def extract_all_keys_occurences(jsons_list,total_rows):
    for each_json in jsons_list:
        json_dict = json.loads(each_json)
        extract_all_keys(json_dict, '')
    print('{0} {1}'.format('Total Rows', total_rows))
    allkeys = _key_occurence_stats.keys()
    for everykey in allkeys:
        percentage_occurence = float((int(_key_occurence_stats[everykey])) / 0.66)
        print('{0} {1} {2} {3}'.format(everykey, ": [", round(percentage_occurence, 2), "%]"))
    return


def extract_specific_key_occurences(jsons_list,total_rows,input_key):
    non_valid_keys = ''
    valid_keys = input_key.split(".")
    given_key = valid_keys[0]
    if len(valid_keys) > 1:
        non_valid_keys = valid_keys[0:-1]
    for each_json in jsons_list:
        json_dict = json.loads(each_json)
        extract_all_values(json_dict, given_key, '', valid_keys, non_valid_keys)
    print('{0} {1}'.format('Total Rows ', total_rows))
    for everystat in _values_of_keys:
        print('{0} {1} {2}'.format(everystat, ", ", _values_of_keys[everystat]))
    return


def main():
    "The main function of the program"
    parser = argparse.ArgumentParser()
    parser.add_argument("--f", help="input the JSON key whose values need to be listed")
    parser.add_argument("filepath", help="input the JSON file path")
    args = parser.parse_args()
    with open(args.filepath) as f:
        jsons_list = f.readlines()
        total_rows = len(jsons_list)
        if args.f:
            extract_specific_key_occurences(jsons_list, total_rows, args.f)
        else:
            extract_all_keys_occurences(jsons_list, total_rows)

            
if __name__ == "__main__": main()
