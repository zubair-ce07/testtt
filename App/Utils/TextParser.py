import nltk
import operator
import math
from itertools import groupby


class TextParser:
    '''This class is responsible for all the text
        processing like counting frequency etc'''

    def noun_n_verb_extractor(self, words):
        words = [word for word in words if len(word) > 2]
        tagged_words = nltk.pos_tag(words)
        word_type = ['NN', 'VB']
        return [word for word, pos in tagged_words if pos in word_type]

    def format_words(self, words):
        extracted_words = self.noun_n_verb_extractor(words)
        return {key: len(list(group)) for key, group in groupby(extracted_words)}

    def generate_sorted_list(self, words_formated):
        words_sorted = sorted(
            words_formated.items(), key=operator.itemgetter(1), reverse=True)
        return words_sorted

    def term_freq_inverse_doc_freq_generator(self, bag_of_words):
        words_formated = {key: len(list(group)) for key, group in groupby(bag_of_words)}
        bag_of_words_count = len(bag_of_words)
        term_frequency = {}

        for word, count in words_formated.items():
            term_frequency[word] = count/float(bag_of_words_count)

        inverse_doc_frequency = words_formated
        n = len(words_formated)
    
        for word, val in inverse_doc_frequency.items():
            inverse_doc_frequency[word] = math.log10(n / float(val))

        term_freq_inverse_doc_freq = {}

        for word, val in term_frequency.items():
            term_freq_inverse_doc_freq[word] = val*inverse_doc_frequency[word]

        return term_freq_inverse_doc_freq
