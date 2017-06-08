import os
import sys
# import os.path


def main():
    valid_flags = ['-e', '-a', '-c']
    if len(sys.argv) < 4:
        print('usage: weatherman.py /path/to/files-dir flag date')
        sys.exit(1)
    elif not sys.argv[1].startswith('/'):
        print('use absolute path for directory containing files.')
        sys.exit(1)
    elif sys.argv[2] not in valid_flags:
        flags = ''
        for flag in valid_flags:
            flags += flag+' '
        print('Invalid flag. Choose a valid flag from:'+flags)
        sys.exit(1)
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    my_path = cur_dir+'/weatherfiles'
    all_files = [f for f in os.listdir(my_path) if os.path.isfile(os.path.join(my_path, f)) and f.endswith('.txt')]

    # for file in all_files:


# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)
if __name__ == '__main__':
    main()