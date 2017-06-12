#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

"""Mimic pyquick exercise -- optional extra exercise.
Google's Python Class

Read in the file specified on the command line.
Do a simple split() on whitespace to obtain all the words in the file.
Rather than read the file line by line, it's easier to read
it into one giant string and split it once.

Build a "mimic" dict that maps each word that appears in the file
to a list of all the words that immediately follow that word in the file.
The list of words can be be in any order and should include
duplicates. So for example the key "and" might have the list
["then", "best", "then", "after", ...] listing
all the words which came after "and" in the text.
We'll say that the empty string is what comes before
the first word in the file.

With the mimic dict, it's fairly easy to emit random
text that mimics the original. Print a word, then look
up what words might come next and pick one at random as
the next work.
Use the empty string as the first word to prime things.
If we ever get stuck with a word that is not in the dict,
go back to the empty string to keep things moving.

Note: the standard python module 'random' includes a
random.choice(list) method which picks a random element
from a non-empty list.

For fun, feed your program to itself as input.
Could work on getting it to put in linebreaks around 70
columns, so the output looks better.

"""

import random
import sys


def mimic_dict(filename):
    """Returns mimic dict mapping each word to list of words which follow it."""
    in_file = open(filename, 'r')
    all_lines = in_file.read()
    in_file.close()
    words = all_lines.split()
    mimicked = {}
    mimicked[' '] = [words[0]]
    for i in range(0, len(words)-1):
        if words[i] in mimicked:
            mimicked[words[i]].append(words[i+1])
        else:
            mimicked[words[i]] = [words[i+1]]
    return mimicked


def print_formatted(in_str, line_break):
    count = 0
    chunk = in_str[:line_break]
    count += line_break
    all_words = []
    all_words.append(chunk)
    all_words.append('\n')
    while(1):
        if len(chunk) < line_break or (count%line_break) != 0:
            break
        else:
            chunk = in_str[count:count+line_break]
            count+=line_break
            all_words.append(chunk)
            all_words.append('\n')

    out_str = ''.join(all_words)
    out_str = out_str[:-2]+'.'
    print('\n'+out_str)


def print_mimic(mimic_d, word):
    """Given mimic dict and start word, prints 200 random words."""
    ITERATIONS = 100
    CUTOFF = 70
    out_str = ''
    for i in range (0, ITERATIONS):
        value_list = []
        if i == 0:
            value_list = mimic_d[' ']
        else:
            string_words = out_str.split()
            cur_word = string_words[-1]
            value_list = mimic_d[cur_word]

        out_str += random.choice(value_list)
        out_str += ' '
    print_formatted(out_str, CUTOFF)


# Provided main(), calls mimic_dict() and mimic()
def main():
    if len(sys.argv) != 2:
        print ('usage: ./mimic.py file-to-read')
        sys.exit(1)

    dict_m = mimic_dict(sys.argv[1])
    print_mimic(dict_m, '')


if __name__ == '__main__':
    main()

