import json
import argparse


def extract_all_keys_occurences(input_tree):
    key_occurence_stats = {}
    for each_value in input_tree:
        parsed_value = json.loads(each_value)
        calculate_key_occurences(parsed_value, '', key_occurence_stats, 1)
    print('Total Rows {0}'.format(len(input_tree)))
    for every_key in key_occurence_stats:
        percentage_occurence = float(((key_occurence_stats[every_key]) / len(input_tree)) * 100)
        print('{0} : [ {1} %]'.format(every_key, round(percentage_occurence, 2)))
    return


def calculate_key_occurences(given_tree_data, parent_key, values_of_keys, variable_type_flag):
    """ Extract all the values from the given tree and store them in values of keys
    If the type flag is on the type of the values are also printed"""
    if isinstance(given_tree_data, dict):
        for each_tree_item in given_tree_data:
            parent_child_heirarchy = parent_key + '.' + each_tree_item if parent_key else each_tree_item
            calculate_key_occurences(given_tree_data[each_tree_item],
                                         parent_child_heirarchy, values_of_keys, variable_type_flag)
    elif isinstance(given_tree_data, list):
        for each_list_item in given_tree_data:
            calculate_key_occurences(each_list_item,
                                     parent_key, values_of_keys, variable_type_flag)
    else:
        extracted_key = parent_key + ":" + str(given_tree_data) + "   " + str(type(given_tree_data))\
            if variable_type_flag else parent_key + ":" + str(given_tree_data)
        values_of_keys[extracted_key] = values_of_keys.get(extracted_key, 0) + 1


def extract_value(json_input, key_heirarchy):
    """ Given a key heirarchy extracts its value in the given json if it exists"""
    if isinstance(json_input, dict):
        if len(key_heirarchy) > 1:
            for each_key in json_input:
                if each_key == key_heirarchy[0] and isinstance(json_input[each_key], (dict, list)):
                    return extract_value(json_input[each_key], key_heirarchy[1:])
            return False
        else:
            for each_key in json_input:
                if each_key == key_heirarchy[0]:
                    return json_input[each_key]
            return False
    elif isinstance(json_input, list):
        values_extracted = []
        for each_value in json_input:
            if isinstance(each_value,(dict, list)):
                values_extracted.append(extract_value(each_value, key_heirarchy))
        if any(values_extracted):
            filter(lambda a: a != False, values_extracted)
            return values_extracted
        else:
            return False
    return False


def calculate_unique_values(input_json_data, input_key):
    """ Given a json list calculates all unique values and their count of the input_key in each json"""
    values_of_keys = {}
    key_heirarchy = input_key.split(".")
    for each_key in input_json_data:
        parsed_json = json.loads(each_key)
        key_heirarchy_value = extract_value(parsed_json, key_heirarchy)
        calculate_key_occurences(key_heirarchy_value, input_key, values_of_keys, 0)
    print('Total Rows  {0}'.format(len(input_json_data)))
    for everystat in values_of_keys:
        print('{0} , {1}'.format(everystat, values_of_keys[everystat]))
    return


def main():
    """ The main function of the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--f", "--input_key", help="input the JSON key whose values need to be listed")
    parser.add_argument("filepath", help="input the JSON file path")
    args = parser.parse_args()
    with open(args.filepath) as f:
        input_json_data = f.readlines()
        calculate_unique_values(input_json_data, args.f) if args.f else extract_all_keys_occurences(input_json_data)

if __name__ == "__main__":
    main()
