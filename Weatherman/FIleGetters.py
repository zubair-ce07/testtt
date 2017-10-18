import os
import calendar
import re


def get_file_names(filename,args):

    directory_files = os.listdir(filename)
    file_names = []
    if re.match("^\d{4}$", args):
        for file_name_row in directory_files:

            if str(args) in file_name_row:
                file_names.append(os.path.join(filename,file_name_row))
        return file_names
    else:
        arg_values = args.split('/')
        for file_name in range(0, len(directory_files)):

            if arg_values[0] in directory_files[file_name] and calendar.month_abbr[int(arg_values[1])] in directory_files[file_name]:
                file_names.append(os.path.join(filename, directory_files[file_name]))
                break

        return file_names