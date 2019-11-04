def remove_nulls(record):
    """removes null values of list"""
    while '' in record:
        record.remove('')
    return record    
def convert_int(record):
    """converts list values int integer"""
    record = list(map(int, record))
    return record
#discard values digit after decimal 55.345345345 to 55.34
def limit_float(number):
    """discard values digit after decimal 55.345345345 to 55.34"""
    return "%.2f" % number
#replace null with 0
def replace_nulls(record):
    """replace null with 0"""
    record = ['0' if element == '' else element for element in record]
    return record

def merge_with_dates(record):
    """returns a list containing maximum records along with date """
    record = replace_nulls(record)
    record = convert_int(record)
    record_index = record.index(max(record)) + 1
    
    return (max(record)), (record_index)        
       