from statistics import mean


def max_value(data, key):
    return max([wr for wr in data if key(wr)], key=key)


def min_value(data, key):
    return min([wr for wr in data if key(wr)], key=key)


def mean_value(data, function):
    avg = int(mean(function(wr) for wr in data if function(wr)))
    return next((wr for wr in data if function(wr) == avg), None)
