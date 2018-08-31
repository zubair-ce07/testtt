from collections import defaultdict


def calculate_words_frequency_from_file(filename, mode):
    """Function read file and make dictionary of word frequencies"""
    words_frequency = defaultdict(int)
    with open(filename, mode) as file:
        for word in file.read().split():
            words_frequency[word] += 1
    return words_frequency


def print_words_frequency(words_frequency):
    """This module will print the dictionary onto console"""
    print ("Word              Frequency")
    print ("---------------------------")
    for key, value in words_frequency.iteritems():
        print key, "               ", value


if __name__ == "__main__":
    words_frequency = calculate_words_frequency_from_file('words.txt', 'r')
    print_words_frequency(words_frequency)
