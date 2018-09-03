import nltk
import operator
import math


class TextParser:
    '''This class is responsible for all the text
        processing like counting frequency etc'''

    def noun_n_verb_extractor(self, words_list):
        tagged_words = nltk.pos_tag(words_list)
        return ([word for word, pos in tagged_words
                if(pos == 'NN' or pos == 'VB') and len(word) > 2])

    def word_frequency_map(self, words_list):
        extracted_words = self.noun_n_verb_extractor(words_list)
        words_dict = {}
        for word in extracted_words:
            words_dict[word] = words_dict.get(word, 1) + 1
        return words_dict

    def generate_sorted_list(self, words_dict):
        sorted_list = sorted(
            words_dict.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_list

    def tfidf_generator(self, bag_of_words):
        words_dict = dict.fromkeys(bag_of_words, 0)
        for word in bag_of_words:
            words_dict[word] += 1
        bag_of_words_count = len(bag_of_words)
        tf_dict = {}
        for word, count in words_dict.items():
            tf_dict[word] = count/float(bag_of_words_count)
        idf_dict = words_dict
        n = len(words_dict)
        for word, val in words_dict.items():
            if val > 0:
                idf_dict[word] += 1
        for word, val in idf_dict.items():
            idf_dict[word] = math.log10(n / float(val))
        tfidf = {}
        for word, val in tf_dict.items():
            tfidf[word] = val*idf_dict[word]
        return tfidf
