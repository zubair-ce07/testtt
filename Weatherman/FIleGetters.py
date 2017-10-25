import os


def get_file_names(directory_path,args):

    directory_files = os.listdir(directory_path)
    file_names = []
    if not args.get('month'):
        for file_name_row in directory_files:

            if args['year'] in file_name_row:

                file_names.append(os.path.join(directory_path,file_name_row))
        return file_names
    else:
        for file_name in directory_files:

            if args["year"] in file_name and args['month'] in file_name:
                file_names.append(os.path.join(directory_path, file_name))
                break

        return file_names
