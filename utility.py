def print_blue(text):
    print("\033[96m{}\033[00m".format(text), end="")


def print_red(text):
    print("\033[31m{}\033[00m".format(text), end="")


def get_file_location(year, month, city, directory):
    file_name = city + "_" + year + "_" + month + ".txt"
    return directory + file_name


def find_max(read_list):
    max = int(read_list[0].max_temp)
    max_index = 0

    for i in range(1, len(read_list)):
        if read_list[i].max_temp != '':
            if max < int(read_list[i].max_temp):
                max = int(read_list[i].max_temp)
                max_index = i

    return [max, max_index]


def find_avg_highest(read_list):
    sum = 0
    divisor = 0

    for i in range(0, len(read_list)):
        if read_list[i].max_temp != '':
            sum += int(read_list[i].max_temp)
            divisor += 1

    return sum / divisor


def find_avg_lowest(read_list):
    sum = 0
    divisor = 0
    for i in range(0, len(read_list)):
        if read_list[i].min_temp != '':
            sum += int(read_list[i].min_temp)
            divisor += 1

    return sum / divisor


def find_avg_mean_humidity(read_list):
    sum = 0
    divisor = 0
    for i in range(0, len(read_list)):
        if read_list[i].mean_humidity != '':
            sum += int(read_list[i].mean_humidity)
            divisor += 1

    return sum / divisor


def find_lowest(read_list):
    min = int(read_list[0].min_temp)
    min_index = 0

    for i in range(1, len(read_list)):
        if read_list[i].min_temp != '':
            if min > int(read_list[i].min_temp):
                min = int(read_list[i].min_temp)
                min_index = i

    return [min, min_index]


def find_max_humidity(read_list):
    max = int(read_list[0].max_humidity)
    max_index = 0

    for i in range(1, len(read_list)):
        if read_list[i].max_humidity != '':
            if max < int(read_list[i].max_humidity):
                max = int(read_list[i].max_humidity)
                max_index = i

    return [max, max_index]
