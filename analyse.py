import argparse
import json
import decimal


def read_files(file_name):
    file_records = []
    result_records = []
    with open(file_name) as f:
        [file_records.append(line) for line in f]
    for obj in file_records:
        try:
            json_to_python_object = json.loads(obj, parse_int=int, parse_float=decimal.Decimal)
            if isinstance(json_to_python_object, list):
                [result_records.append(sub_object) for sub_object in json_to_python_object]
            elif isinstance(json_to_python_object, dict):
                result_records.append(json_to_python_object)
        except ValueError:
            print("data was not valid JSON")
    return convert(result_records)


def convert(records):
    if isinstance(records, dict):
        return {convert(key): convert(value) for key, value in records.iteritems()}
    elif isinstance(records, list):
        return [convert(element) for element in records]
    elif isinstance(records, unicode):
        return records.encode('utf-8')
    else:
        return records


def get_fieldnames_datatype(all_records):
    target_values = []
    target_values.sort()
    for single_record in all_records:
        for field_name in single_record.keys():
            if isinstance(single_record[field_name], dict):
                target_values.append([field_name, type(single_record[field_name]).__name__])
                target_values += (
                    iterate_nested_dictionary(single_record[field_name], single_record[field_name].keys(), field_name))
            elif isinstance(single_record[field_name], list):
                target_values.append([field_name, type(single_record[field_name]).__name__])
                for nested_list_elements in single_record[field_name]:
                    if isinstance(nested_list_elements, dict):
                        target_values += iterate_nested_dictionary(single_record[field_name],
                                                                   single_record[field_name].keys(), field_name)
            else:
                target_values.append([field_name, type(field_name).__name__])
    filtered_list = list(eliminate_duplicate(target_values))
    return filtered_list


def iterate_nested_dictionary(single_record, field_names, fieldname_prefix):
    result_values = []
    for value in field_names:
        if value in single_record.keys():
            sub_record = single_record[value]
            if isinstance(sub_record, dict):
                result_values.append([fieldname_prefix + "." + value, type(sub_record).__name__])
                for key_value in sub_record.keys():
                    leaf_node_name_prefix = fieldname_prefix + "." + value + "." + key_value
                    result_values.append([leaf_node_name_prefix, type(sub_record[key_value]).__name__])
                    nested_result = (iterate_nested_dictionary(sub_record,
                                                               key_value,
                                                               fieldname_prefix + "." +
                                                               value))
                    result_values += nested_result
    return result_values


def eliminate_duplicate(result_values):
    found = set()
    for item in result_values:
        if item[0] not in found:
            yield item
            found.add(item[0])


def get_all_fill_rates(all_records, fields_datatype_records):
    all_fill_rates = []
    for field_name, data_type in fields_datatype_records:
        filtered_field_name = field_name.split(".")
        fieldname_postfix = filtered_field_name[-1]
        empty_fields = 0
        total_occurrence = 0
        for record in all_records:
            if iterate_nested_record(record, fieldname_postfix):
                if iterate_nested_record(record, fieldname_postfix) == 'empty_fields':
                    empty_fields += 1
                total_occurrence += 1
            filled = total_occurrence - empty_fields
        if total_occurrence >= 1:
            fill_rate = (filled / float(total_occurrence)) * 100
            all_fill_rates.append([field_name, data_type, fill_rate])
    return eliminate_duplicate(all_fill_rates)


def print_fill_rates(all_fill_rates):
    for field_name, data_type, fill_rate in all_fill_rates:
        print(field_name + " " + data_type + " Fill rate: " + str(fill_rate) + " %")


def iterate_nested_record(records, key_value):
    if (key_value in records.keys()):
        if not records[key_value]:
            return "empty_fields"
        else:
            return records[key_value]
    stack = records.items()
    try:
        while stack:
            k, v = stack.pop()
            if isinstance(v, list) or isinstance(v, dict):
                if key_value in v.keys():
                    if not v[key_value]:
                        return "empty_fields"
                    else:
                        return v[key_value]
                if isinstance(v, list) or isinstance(v, dict):
                    stack.extend(v.items())
            else:
                if k == key_value:
                    return v
    except:
        return False


def analyse_complex_record(all_records, fieldnames_datatype):
    result_structure = {}
    for field_name in fieldnames_datatype:
        field_name = field_name.split(".")[-1]
        results = []
        for record in all_records:
            if field_name in record.keys():
                sub_class = record[field_name]
                if isinstance(sub_class, str) or isinstance(sub_class, bool):
                    results.append(sub_class)
                elif isinstance(sub_class, list):
                    results += sub_class
                elif isinstance(sub_class, dict):
                    results += sub_class.keys()
                else:
                    return
        json_summary = get_unique_values(results)
        result_structure[field_name] = json_summary
    return result_structure


def get_unique_values(items):
    results = {}
    for item in items:
        if item not in results:
            results[item] = 1
        else:
            results[item] += 1
    return results


def sort_records(reocrds_list):
    if isinstance(reocrds_list, dict):
        reocrds_list = [(k, v) for v, k in sorted(
            [(v, k) for k, v in reocrds_list.items()], reverse=True
        )
                        ]
    return reocrds_list


def search_in_nested_records(json_obj, key_value):
    if key_value in json_obj.keys():
        return json_obj[key_value]
    stack = json_obj.items()
    while stack:
        k, v = stack.pop()
        if isinstance(v, list) or isinstance(v, dict):
            stack.extend(v.items())
        else:
            if k == key_value:
                return v


def print_field_fillrate(fill_rates,field_name):
    for field,data_type,fillrate in fill_rates:
        if(field==field_name):
            print(field_name + " " + data_type +
                  " Fill rate: " + str(fillrate) +
                  " %"
                  )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--field_argument", nargs="?", type=str)
    parser.add_argument("file_name", help="Path of folder")
    argument = parser.parse_args()
    file_name = argument.file_name
    all_records = read_files(file_name)
    fieldnames_datatype_records = get_fieldnames_datatype(all_records)
    fill_rates = get_all_fill_rates(all_records, fieldnames_datatype_records)
    total_length = len(all_records)
    print ("Number of rows are :" + str(total_length))
    if argument.field_argument:
        field_names = [x[0] for x in fieldnames_datatype_records]
        field_counter_result = analyse_complex_record(all_records, field_names)
        result = search_in_nested_records(field_counter_result, argument.field_argument)
        print_field_fillrate(fill_rates,argument.field_argument)
        sorted_result = sort_records(result)
        print (sorted_result)

    else:
        print_fill_rates(fill_rates)
