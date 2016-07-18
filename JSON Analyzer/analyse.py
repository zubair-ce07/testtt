import json
import argparse

_key_occurence_stats = dict()
_values_of_keys = dict()


def extract_all_keys(dict_):
    "Function that extracts all the keys of a dictionary at all levels"
    for key in dict_:
        if key in _key_occurence_stats:
            _key_occurence_stats[key] += 1
        else:
            _key_occurence_stats[key] = 1
        if type(dict_[key]) is dict:
            extract_all_keys(dict_[key])
    return


def extract_all_values(dict_, key, key_flag):
    "Function that extracts all the values of a dictionary at all levels"
    for each_key in dict_:
        if (each_key == key or key_flag):
            value = dict_[each_key]
            if type(value) is list:
                for my_string in value:
                    if my_string in _values_of_keys:
                        _values_of_keys[my_string] += 1
                    else:
                        _values_of_keys[my_string] = 1
            elif type(value) is dict:
                for my_string in value:
                    if type(value[my_string]) is dict:
                        extract_all_values(value,my_string,1)
                    elif type(value[my_string]) is list:
                        extract_all_values(value,my_string,1)
                    else:
                        my_key=my_string+":"+str(value[my_string])
                        if my_key in _values_of_keys:
                            _values_of_keys[my_key] += 1
                        else:
                            _values_of_keys[my_key] = 1
            else:
                if value in _values_of_keys:
                    _values_of_keys[value] += 1
                else:
                    _values_of_keys[value] = 1
        else:
            if type(dict_[each_key]) is dict:
                extract_all_values(dict_[each_key],key,0)
    return


def main():
    "The main function of the program"
    parser = argparse.ArgumentParser()
    parser.add_argument("--f", help="input the JSON key whose values need to be listed")
    parser.add_argument("filepath", help="input the JSON file path")
    args = parser.parse_args()
    with open(args.filepath) as f:
        jsons = f.readlines()
        Count = len(jsons)
        if args.f:
            key_ = args.f
            splitted = key_.split(".")
            given_key = splitted[-1]
            for each_json in jsons:
                parsed_dict  = json.loads(each_json)
                # extract all the values and their count corresponding to the key args.f
                extract_all_values(parsed_dict, given_key,0)
            print '{0} {1}'.format("Total Rows ",str(Count))
            print key_
            allstats = _values_of_keys.keys()
            for everystat in allstats:
                print '{0} {1} {2}'.format(everystat,", ", str(_values_of_keys[everystat]))
        else:
            for each_json in jsons:
                parsed_dict = json.loads(each_json)
                extract_all_keys(parsed_dict)
            print '{0} {1}'.format("Total Rows",str(Count))
            allkeys = _key_occurence_stats.keys()
            for everykey in allkeys:
                perc = float((int(_key_occurence_stats[everykey])) / 0.66)
                print '{0} {1} {2} {3}'.format(everykey,": [",str(perc),"%]")

if __name__ == "__main__": main()
