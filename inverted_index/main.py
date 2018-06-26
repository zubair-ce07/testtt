__author__ = 'abdul'

import sys

import argparse

import inverted_index

def check_arg(args=None):
    """
    Takes arguments as input
    """
    parser = argparse.ArgumentParser(description='Search Engine')
    parser.add_argument('-s', '--string',
                        help='Comma seperated strings to search in stored data. ',
                        required='True',
                        type=str)
    results = parser.parse_args(args)
    return (results.string)

if __name__ == '__main__':
    strings = check_arg(sys.argv[1:]) # Receive arguments
    index = inverted_index.InvertedIndex()

    try:
        index.load_inverted_index()
        index.search_inverted_index(strings.split(','))
    except (FileNotFoundError, IndexError) as e:
        print(format(e))
