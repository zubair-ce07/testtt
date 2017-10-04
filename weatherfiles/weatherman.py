import sys
import os
import fnmatch

def weatherman():
    return


def get_filenames_from_dir(dir, year):
    filenames = []
    for file in os.listdir(dir):
        if fnmatch.fnmatch(file, 'Murree_weather_' + year + '_*.txt'):
            filename = os.path.join(dir, file)
            filenames.append(filename)
    return filenames


def read_files(filenames):
    filesdata = {}
    for filename in filenames:
        filedata = open(filename, 'rU').readlines()
        filesdata[filename] = filedata
    return filesdata


def read_files_from_path(dir, year):
    filenames = get_filenames_from_dir(dir, year)
    filesdata = read_files(filenames)
    print(filesdata)
    return


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('''usage: weatherman.py /path/to/files-dir -option year [-option year] [-option year]
        options: -a, -e, -c''')
        sys.exit(1)

    read_files_from_path(args[0], args[2])

if __name__ == '__main__':
    main()