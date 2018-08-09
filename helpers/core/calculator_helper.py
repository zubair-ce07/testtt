def month_with_num(num):
    num = int(num)
    month = None
    if num == 1:
        month = 'Jan'
    elif num == 2:
        month = 'Feb'
    elif num == 3:
        month = 'Mar'
    elif num == 4:
        month = 'Apr'
    elif num == 5:
        month = 'May'
    elif num == 6:
        month = 'Jun'
    elif num == 7:
        month = 'Jul'
    elif num == 8:
        month = 'Aug'
    elif num == 9:
        month = 'Sep'
    elif num == 10:
        month = 'Oct'
    elif num == 11:
        month = 'Nov'
    elif num == 12:
        month = 'Dec'
    return month


def cal_average(list_):
    return round(sum(list_) / float(len(list_)), 2)


def find_keys_in_arr(key, arr):
    # getting a specific keys from a list of dicts
    # returns list
    return [int(d[key]) for d in arr if key in d]
