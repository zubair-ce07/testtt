"""
This Module Counts the frequency of words.

This module has a class which prints words in
file "words.txt" along with their frequency.
"""

import re
import logging
from collections import defaultdict


class WordFrequencyCounter:
    """
    Counts the frequency of words and prints results
    """
    
    def __init__(self):
        """
        Reads "utf-8" encoded file and compile the regex.
        """

        # compiling regex for alphanumeric words
        self._filter = re.compile(r'\b\w+\b')

        self._input_data = ''
        logging.basicConfig(format='%(levelname)s: %(message)s')

        try:
            # opening file and assuming file has encoding "utf-8"
            # if encoding is not "utf-8" ignoring errors
            with open('words.txt', 'r') as input_file:
                self._input_data = input_file.read()

        except FileNotFoundError:
            logging.error('File "words.txt" not Found.')

        except UnicodeDecodeError:
            logging.error('Encoding of file is not "utf-8"')

    def _calculate_frequency(self):
        """
        Calculate how many times a word is occurring in the input data.
        """

        # initializing dictionary
        word_frequency = defaultdict(int)

        for word in self._filter.finditer(self._input_data):
            # group of characters matched regex.
            matched_word = word.group()

            # increase frequency of word by 1
            word_frequency[matched_word] += 1

        return word_frequency

    def print_results(self):
        """
        prints words along with their occurrences.
        """

        if len(self._input_data) is 0:
            print('No data read from file.')
            return

        # get a calculated dictionary with frequency and words
        word_frequency = self._calculate_frequency()

        print('{:35s}'.format('Word'), 'Frequency')
        print('-'*45)

        for word, frequency in word_frequency.items():
            print('{word:35s}'.format(word=word), frequency)


if __name__ == '__main__':
    wfc = WordFrequencyCounter()
    wfc.print_results()
