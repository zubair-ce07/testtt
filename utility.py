def print_blue(text, n):
    print("\033[96m{}\033[00m".format(text) * n, end="")


def print_red(text, n):
    print("\033[31m{}\033[00m".format(text) * n, end="")


def get_file_location(year, month, city, directory):
    file_name = city + "_" + str(year) + "_" + month + ".txt"
    return directory + "/" + file_name
