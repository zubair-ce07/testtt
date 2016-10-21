import argparse
import json
import decimal


def read_files(filename):
    """This function read json file line by line and
       return the JSOn to  python format objects list.
    :param filename:Takes name file an read it line by line
    :return: The list python objects
    """
    file_records = []
    result_records = []
    with open(filename) as f:
        for line in f:
            file_records.append(line)
    for obj in file_records:
        try:
            json_to_python_object = json.loads(obj, parse_int=int, parse_float=decimal.Decimal)
            if isinstance(json_to_python_object, list):
                for sub_object in json_to_python_object:
                    result_records.append(sub_object)
            elif isinstance(json_to_python_object, dict):
                result_records.append(json_to_python_object)
        except ValueError:
            print("data was not valid JSON")
    return result_records


def get_fieldnames_datatype(all_records):
    """Method takes records and return fieldname with their datatypes.
    """
    target_values = []
    for single_record in all_records:
        for field_name in single_record.keys():
            if isinstance(single_record[field_name], dict):
                target_values.append([field_name, type(single_record[field_name]).__name__])
                target_values += analyse_nested_structure(single_record[field_name],
                                                          single_record[field_name].keys(),
                                                          field_name
                                                          )
            elif isinstance(single_record[field_name], list):
                target_values.append([field_name, type(single_record[field_name]).__name__])
                for nested_list_elements in single_record[field_name]:
                    if isinstance(nested_list_elements, dict):
                        target_values += analyse_nested_structure(nested_list_elements,
                                                                  nested_list_elements.keys(),
                                                                  field_name
                                                                  )
            else:
                target_values.append([field_name, type(field_name).__name__])
    filtered_list = list(eliminate_duplicate(target_values))
    return filtered_list


def analyse_nested_structure(single_record, field_names, fieldname_prefix):
    """
    This method take nested dictionary field name and parent node name and
    itrerate upto leaf nodes and retrun leaf node(Fieldname) and its datatype
    :param single_record: The single record that have a nested structure.
    :param field_names: The name of all the fileds in dictionary.
    :param fieldname_prefix: Name of parent node that is append with each child fieldname.
    :return: All the leaf nodes with well formated name like grnad_parent.parent.child_Field.
    """
    result_values = []
    for value in field_names:
        if value in single_record.keys():
            sub_record = single_record[value]
            if isinstance(sub_record, dict):
                result_values.append([fieldname_prefix + "." + value, type(sub_record).__name__])
                for key_value in sub_record.keys():
                    leaf_node_name_prefix = fieldname_prefix + "." + value + "." + key_value
                    result_values.append([leaf_node_name_prefix, type(sub_record[key_value]).__name__])
                    nested_result = analyse_nested_structure(sub_record, key_value,
                                                             fieldname_prefix + "." +
                                                             value)

                    result_values += nested_result
            else:
                result_values.append([fieldname_prefix + "." + value, type(sub_record).__name__])
    return result_values


def eliminate_duplicate(result_values):
    """In our each line has json object with few same fieldname.
       There may case field names from each record object cause
       duplications.
    """
    found = set()
    for item in result_values:
        if item[0] not in found:
            yield item
            found.add(item[0])


def get_all_fill_rates(all_records, fields_datatype_records):
    """Method takes alll the reocrds and their fieldnames
       and then Calculate the occurance of each field and Calculate
       the fill rate of all field name.
    :param all_records: The list of all records.
    :param fields_datatype_records:Fields name with their data type.
    :return: List of fillrate of all fields.
    """
    all_fill_rates = []
    for field_name, data_type in fields_datatype_records:
        filtered_field_name = field_name.split(".")
        fieldname_postfix = filtered_field_name[-1]
        empty_fields = 0
        total_occurrence = 0
        for record in all_records:
            search_results = iterate_nested_record(record, fieldname_postfix)
            if search_results:
                if search_results is None:
                    empty_fields += 1
                total_occurrence += 1
            filled = total_occurrence - empty_fields
        if total_occurrence >= 1:
            fill_rate = (filled / float(total_occurrence)) * 100
            all_fill_rates.append([field_name, data_type, fill_rate])
    return eliminate_duplicate(all_fill_rates)


def print_fill_rates(all_fill_rates):
    """This method prints all the fill rates."""
    for field_name, data_type, fill_rate in all_fill_rates:
        print(field_name + " " + data_type + " Fill rate: " + str(fill_rate) + " %")


def iterate_nested_record(records, search_key):
    """This method walkin the nested dictionary and
       search the key and and its value.
    :param records: Take a record that may have nested dictioanries.
    :param search_key: The values to be search.
    :return: bool value: In case key is not found in our structure return false to calling function.
    """
    if search_key in records.keys():
        if not records[search_key]:
            return None
        else:
            return records[search_key]
    stack = records.items()
    try:
        while stack:
            recordkey, recordvalue = stack.pop()
            if isinstance(recordvalue, list) or isinstance(recordvalue, dict):
                if search_key in recordvalue.keys():
                    if not recordvalue[search_key]:
                        return None
                    else:
                        return recordvalue[search_key]
                stack.extend(recordvalue.items())
            else:
                if recordkey == search_key:
                    return recordvalue
    except:
        return False


def sort_records(records_list):
    """This method sorts the dictionaries on the basis of their values
       in reverse order
    :param records_list: unsorted values.
    :return: Sort the record and return sot
    """
    if isinstance(records_list, dict):
        records_list = [(recordkey, recordvalue) for recordvalue, recordkey in sorted(
            [(recordvalue, recordkey) for recordkey, recordvalue in records_list.items()], reverse=True
        )
                        ]
    return records_list


def print_field_fillrate(fill_rates, field_name):
    """This Method prints the fill rate of specific fieldname"""
    for field, data_type, fillrate in fill_rates:
        if field == field_name:
            print(field_name + " " + data_type + " Fill rate: " + str(fillrate) + " %")


def get_field_counts(input_values, all_records):
    """ This method calculate the the occurrence of field value
    :param input_values: the name of field
    :param all_records: the list of all records
    :return: the sorted list of fieldname with with values count
    """
    sub_record = []
    for record in all_records:
        key_found = True
        input_fields = input_values.split(".")
        for field_name in input_fields:
            if isinstance(record, dict):
                if field_name in record.keys():
                    record = record[field_name]
                else:
                    key_found = False
            else:
                record = None
        if key_found:
            if isinstance(record, str) or isinstance(record, bool):
                sub_record.insert(0, record)
            elif isinstance(record, list):
                sub_record += record
            elif isinstance(record, dict):
                sub_record += record.keys()
    sub_record = dict((x, sub_record.count(x)) for x in set(sub_record))
    return sort_records(sub_record)


def print_field_counter(all_field_counter):
    """ Method takes list of all field counter and print them"""
    for field_count in all_field_counter:
        print field_count


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
        print_field_fillrate(fill_rates, argument.field_argument)
        field_counter = get_field_counts(argument.field_argument, all_records)
        print_field_counter(field_counter)
    else:
        print_fill_rates(fill_rates)
