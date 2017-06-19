"""
This module is a word finder.

This module finds occurrences of user provided word in input.txt.
Also provides with the indexes of each occurrences.
"""

import re
import logging


# input for word to search
word_to_find = input('Enter the word you want to search: ')

# compiling regular expression
matcher = re.compile(word_to_find)

input_data = ''

try:
    # reading file to which search word from
    with open('input.txt', 'r') as input_file:
        input_data = input_file.read()

except FileNotFoundError:
    logging.error('File "input.txt" not Found.')

# creating list of matched words
occurrences = [match for match in matcher.finditer(input_data)]

# outputting how many times word occurred and at what index
print('Total Occurrences: ', len(occurrences))

for occurrence in occurrences:
    print('At index: ', occurrence.span())
