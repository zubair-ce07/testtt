import json
import argparse


def extract_all_keys_occurences(jsons_list, total_rows):
    key_occurence_stats = {}
    for each_json in jsons_list:
        parsed_json = json.loads(each_json)
        calculate_key_occurences(parsed_json, '', key_occurence_stats,1)
    print('Total Rows {0}'.format(total_rows))
    for everykey in key_occurence_stats:
        percentage_occurence = float(((key_occurence_stats[everykey]) / total_rows) * 100)
        print('{0} : [ {1} %]'.format(everykey, round(percentage_occurence, 2)))
    return


def calculate_key_occurences(given_tree_data, parent_key, values_of_keys,type_flag):
    """ Extract all the values from the given tree and store them in values of keys
    If the type flag is on the type of the values are also printed"""
    if isinstance(given_tree_data, dict):
        for each_key_of_json in given_tree_data:
            if parent_key:
                calculate_key_occurences(given_tree_data[each_key_of_json],
                                     parent_key + '.' + each_key_of_json, values_of_keys,type_flag)
            else:
                calculate_key_occurences(given_tree_data[each_key_of_json],
                                         parent_key + each_key_of_json, values_of_keys,type_flag)
    elif isinstance(given_tree_data, list):
        for each_list_item in given_tree_data:
            calculate_key_occurences(each_list_item,
                                     parent_key, values_of_keys,type_flag)
    else:
        if type_flag:
            extracted_key = parent_key + ":" + str(given_tree_data) + "   " + str(type(given_tree_data))
        else:
            extracted_key = parent_key + ":" + str(given_tree_data)
        if extracted_key in values_of_keys:
            values_of_keys[extracted_key] += 1
        else:
            values_of_keys[extracted_key] = 1


def flatten(nested_list):
    for each_item in nested_list:
        if isinstance(each_item, (list,tuple)):
            for each_sub_item in flatten(each_item):
                yield each_sub_item
        else:
            yield each_item


def extract_value(json_input, key_heirarchy):
    """ Given a key heirarchy extracts its value in the given json if it exists"""
    if len(key_heirarchy) > 1:
        if isinstance(json_input, dict):
            for each_key in json_input:
                if each_key == key_heirarchy[0] and isinstance(json_input[each_key], (dict,list)):
                    return extract_value(json_input[each_key], key_heirarchy[1:])
            return False
        elif isinstance(json_input, list):
            values_extracted = []
            for each_value in json_input:
                if isinstance(each_value,(dict,list)):
                    values_extracted.append(extract_value(each_value,key_heirarchy))
            if any(values_extracted):
                filter(lambda a: a != False, flatten(values_extracted))
                return values_extracted
            else:
                return False
    elif len(key_heirarchy) == 1:
        if isinstance(json_input, dict):
            for each_key in json_input:
                if each_key == key_heirarchy[0]:
                    return json_input[each_key]
            return False
        elif isinstance(json_input, list):
            subvalues_extracted = []
            for each_value in json_input:
                if isinstance(each_value, (dict,list)):
                    subvalues_extracted.append(extract_value(each_value, key_heirarchy))
            if any(subvalues_extracted):
                filter(lambda a: a != False, flatten(subvalues_extracted))
                return subvalues_extracted
            else:
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
            if isinstance(key_heirarchy_value,list):
                for each_extracted_value in key_heirarchy_value:
                    calculate_key_occurences(each_extracted_value, input_key, values_of_keys,0)
            else:
                calculate_key_occurences(key_heirarchy_value, input_key, values_of_keys,0)
    print('Total Rows  {0}'.format(total_rows))
    for everystat in values_of_keys:
        print('{0} ,  {1}'.format(everystat, values_of_keys[everystat]))
    return


def main():
    """ The main function of the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--f","--input_key", help="input the JSON key whose values need to be listed")
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
