import nltk
import operator


class TextProcessor:
    '''This class is responsible for all the text
        processing like counting frequency etc'''

    def noun_n_verb_extractor(self, words_list):
        tagged_words = nltk.pos_tag(words_list)
        return ([word for word, pos in tagged_words
                if(pos == 'NN' or pos == 'VB') and len(word) > 2])

    def dictionary_generator(self, words_list):
        extracted_words = self.noun_n_verb_extractor(words_list)
        words_dict = {}
        for word in extracted_words:
            if words_dict.get(word):
                words_dict[word] = sum(words_dict[word], 1)
            else:
                words_dict[word] = 1
        return words_dict

    def generate_sorted_list(self, words_dict):
        sorted_list = sorted(
            words_dict.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_list

    def tfidf_genrator(self, corpus):
        pass
