import json
import argparse
import os.path
import collections



def rate_by_search_key(data_line, record, Resultdict, search_key): # this function is used for count element rate which is given as search key  in given json files
    if search_key in data_line:
        if data_line.get(search_key):
            key = search_key
            if key not in record:
                record[key] = {'type': type(data_line[search_key]).__name__,
                               'count': 1} 
            else:
                record[key]['count'] += 1
            if isinstance(data_line[search_key], list):
                for data in data_line[search_key]:
                    if (isinstance(data, dict)):
                        node_name = tuple(data.keys())
                    else:
                        node_name = tuple(data_line[search_key])
            elif isinstance(data_line[search_key], dict):
                node_name = tuple(data_line[search_key].keys())
            else:
                node_name = data_line[search_key]
            if node_name in Resultdict:
                Resultdict[node_name] += 1
            else:
                Resultdict[node_name] = 1


def get_element_rate(data_line, record, sub_param=''): # this function is used for count elements rate in given json files
    for node_name in data_line:
        if data_line[node_name]:
            key = node_name if sub_param == '' else sub_param + '.' + node_name
            if key not in record:  
                record[key] = {'type': type(data_line[node_name]).__name__,
                               'count': 1}
            else:
                record[key]['count'] += 1
            if isinstance(data_line[node_name], list):
                for node_select in data_line[node_name]:
                    if isinstance(node_select, dict):
                        get_element_rate(node_select, record, key)
            if isinstance(data_line[node_name], dict):
                get_element_rate(data_line[node_name], record, key)


def print_data(record, total_rows, Resultdict):
    percentage = 0.0

    if Resultdict:
        print '['
        for key in sorted(Resultdict.iterkeys()):
            print "%s: %s" % (key, Resultdict[key])
        print ']'
    print 'Total Rows:', total_rows
    record = collections.OrderedDict(sorted(record.items()))
    if record:
        for data in record:
            percentage = (record[data]['count'] * 100) / total_rows
            print data, ':', record[data]['count'], record[data]['type'], \
                '[', str(percentage), '%]'
    else:
        print "No Record Found"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help='Json file Name')
    parser.add_argument('-f', help='Must be present while using Search by key')
    args = parser.parse_args()
    record = {}
    total_rows = 0
    Resultdict = {}
    search_key_argument = args.f
    file_name = args.file_name
    if file_name.endswith('.json') \
            and os.path.isfile(file_name):
        with open(file_name, "r") as jsonfile: # json file reads
            for line in jsonfile:
                total_rows += 1
                jsondecode = json.loads(line)
                if (search_key_argument is None):
                    get_element_rate(jsondecode, record)
                else:
                    if '.' in search_key_argument:
                        search_key = search_key_argument.split('.')
                        search = search_key.pop()
                        data_line = jsondecode
                        for element in search_key:
                            if element not in data_line:
                                continue
                            if isinstance(data_line[element], list): # if data_element (given json node) is list type
                                for list_data in data_line[element]: 
                                    if (len(search_key) > 1):
                                        research = search_key.pop()
                                        for all_list_data in data_line[element]:
                                            if research in all_list_data:
                                                for data_list in all_list_data[research]:
                                                    rate_by_search_key(data_list, record,
                                                                       Resultdict, search)

                                    else:
                                        data_line = list_data
                                        rate_by_search_key(data_line, record,
                                                           Resultdict, search)

                            else:
                                data_line = data_line[element]
                                rate_by_search_key(data_line, record,
                                                   Resultdict, search)
                    else:
                        rate_by_search_key(jsondecode, record,
                                           Resultdict, search_key_argument)
    else:
        print "Error in File Name!"
    print_data(record, total_rows, Resultdict)


if __name__ == "__main__":
    main() # main function
