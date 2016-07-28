import json
import argparse


def extract_all_keys(given_dictionary, previous_key, key_occurence_stats):
    """Function that extracts all the keys of a dictionary at all levels"""
    for each_key in given_dictionary:
        key = previous_key+each_key
        if key in key_occurence_stats:
            key_occurence_stats[key] += 1
        else:
            key_occurence_stats[key] = 1
        if isinstance(given_dictionary[each_key],dict):
            extract_all_keys(given_dictionary[each_key],
                             key + '.', key_occurence_stats)
    return


def extract_all_keys_occurences(jsons_list, total_rows):
    key_occurence_stats = {}
    for each_json in jsons_list:
        parsed_json = json.loads(each_json)
        extract_all_keys(parsed_json, '', key_occurence_stats)
    print('{0} {1}'.format('Total Rows', total_rows))
    for everykey in key_occurence_stats:
        percentage_occurence = float(((key_occurence_stats[everykey]) / total_rows) * 100)
        print('{0} {1} {2} {3}'.format(everykey, ": [", round(percentage_occurence, 2), "%]"))
    return


def calculate_key_occurences(given_tree_data, parent_key, values_of_keys):
    """extract all the values from the given tree and store them in values of keys"""
    if isinstance(given_tree_data, dict):
        for each_key_of_json in given_tree_data:
            calculate_key_occurences(given_tree_data[each_key_of_json],
                                     parent_key + '.' + each_key_of_json, values_of_keys)
    elif isinstance(given_tree_data, list):
        for each_list_item in given_tree_data:
            count = 0
            calculate_key_occurences(each_list_item,
                                     parent_key + "[" + str(count) + "]", values_of_keys)
            count += 1
    else:
        extracted_key = parent_key+":"+str(given_tree_data)
        if extracted_key in values_of_keys:
            values_of_keys[extracted_key] += 1
        else:
            values_of_keys[extracted_key] = 1


def extract_value(json_dict, key_heirarchy):
    """given a key heirarchy extracts its value in the given json if it exists"""
    if (len(key_heirarchy) > 1):
        for each_key in json_dict:
            if (each_key == key_heirarchy[0] and isinstance(json_dict[each_key], dict)):
                return extract_value(json_dict[each_key], key_heirarchy[1:])
        return False
    elif (len(key_heirarchy) == 1):
        for each_key in json_dict:
            if (each_key == key_heirarchy[0]):
                return json_dict[each_key]
        return False
    return False


def calculate_unique_values(jsons_list, total_rows, input_key):
    """ Given a json list calculates all unique values and their count of the input_key in each json"""
    values_of_keys = {}
    key_heirarchy = input_key.split(".")
    for each_json in jsons_list:
        parsed_json = json.loads(each_json)
        key_heirarchy_value = extract_value(parsed_json, key_heirarchy)
        if key_heirarchy_value:
            calculate_key_occurences(key_heirarchy_value, input_key, values_of_keys)
    print('{0} {1}'.format('Total Rows ', total_rows))
    for everystat in values_of_keys:
        print('{0} {1} {2}'.format(everystat, ", ", values_of_keys[everystat]))
    return


def main():
    """The main function of the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--f", help="input the JSON key whose values need to be listed")
    parser.add_argument("filepath", help="input the JSON file path")
    args = parser.parse_args()
    with open(args.filepath) as f:
        jsons_list = f.readlines()
        total_rows = len(jsons_list)
        if args.f:
            calculate_unique_values(jsons_list, total_rows, args.f)
        else:
            extract_all_keys_occurences(jsons_list, total_rows)


if __name__ == "__main__":
    main()
