import os,calendar


def get_file_names(args):

    directory_files = os.listdir(args.filename)
    file_names_list = []

    for file_name in range(0, len(directory_files)):

        if args.e in directory_files[file_name]:
            file_names_list.append(args.filename + '/' + directory_files[file_name])

    return file_names_list


def get_file_names_one(args):

    directory_files = os.listdir(args.filename)
    file_names_list = []

    if len(args.a) == 6:
        month = int(args.a[5:6])
    else:
        month = int(args.a[5:7])

    for file_name in range(0, len(directory_files)):

        if args.a[0:4] in directory_files[file_name] and calendar.month_abbr[month] in directory_files[file_name]:

            file_names_list.append(args.filename + '/' + directory_files[file_name])

    return file_names_list


def get_file_names_two(args):

    directory_files = os.listdir(args.filename)
    file_names_list = []

    month = int(args.c[5:7])

    for file_name in range(0, len(directory_files)):

        if args.c[0:4] in directory_files[file_name] and calendar.month_abbr[month] in directory_files[file_name]:
            file_names_list.append(args.filename + '/' + directory_files[file_name])
            break

    return file_names_list


