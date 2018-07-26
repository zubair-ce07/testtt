"""
Using member functions provided by the class WordAnalysis, you can
extract word counts and print out the results in a readable fashion
"""

import re
from collections import defaultdict


class WordAnalysis(object):
    """
    Holds methods to calculate the frequency of words in a file and
    printing the result in a pretty format
    """

    def __init__(self, file_name, mono_case=False):
        """
        Arguments:
            file_name (str): Filename for the candidate file
            mono_case (bool): It true then lowercase = uppercase
        """

        self.file_name = file_name
        self.mono_case = mono_case

    def _calculate_word_frequency_in_file(self):
        """
        Reads the txt file and does frequency calculation for each word
        """

        word_pattern = r'[a-zA-Z]+'
        self.word_frequency_map = defaultdict(int)

        try:
            with open(self.file_name, encoding="utf-8") as input_file:
                matching_words = re.findall(word_pattern, input_file.read())

            for word in matching_words:
                word = word.lower() if self.mono_case else word
                self.word_frequency_map[word] += 1

        except OSError as error_message:
            print(error_message)
        except UnicodeDecodeError:
            print("Bad encoding type, UTF-8 is preffered")

    def print_word_frequency(self):
        """
        Calculates the word frequency from the file and prints the
        output to the console
        """

        self._calculate_word_frequency_in_file()
        if self.word_frequency_map.keys():
            spacing_steps = 16
            print('{:<{}}{}'.format("Word", spacing_steps, "Frequency"))
            print('-'*28)
            for word, frequency in self.word_frequency_map.items():
                print('{:<{}}{}'.format(word, spacing_steps, frequency))


def main():
    test1 = WordAnalysis("words_test.txt")
    test1.print_word_frequency()


if __name__ == "__main__":
    main()
