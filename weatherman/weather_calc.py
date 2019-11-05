import re
from file_helper import convert_int, remove_nulls
from file_helper import replace_nulls


def get_max_value(record):
    """returns maximum value"""
    record = remove_nulls(record)
    record = convert_int(record)
    return max(record)

def get_min_value(record):
    """returns minimum value"""
    record = remove_nulls(record)
    record = convert_int(record)
    return min(record)

def get_average(record):
    """returns average"""
    record = remove_nulls(record)
    record = convert_int(record)
    return sum(record) / len(record )    

def highest_temp(record):
    """returns highest tempratures of all over the year"""
    max_temp_index = (record.index(max(record)))
    record = record[max_temp_index]
    
    digit = record[5:7]
    digit = re.sub('\W+','', digit)
    
    if(int(digit)<10):
        return record[1:3], record[7:11] + " " + record[5:7]
    else:
        return record[1:3], record[8:11] + " " + record[5:7]

def lowest_temp(record):
    """returns lowest tempratures of all over the year"""
    min_temp_index = (record.index(min(record)))
    record = record[min_temp_index]
    
    digit = record[5:7]
    digit = re.sub('\W+','', digit)
    
    if(int(digit)<10):
        return record[1:3], record[7:11] + " " + record[5:6]
    else:
        return record[1:3], record[8:11] + " " + record[5:7]        