import nltk


class TextProcessor:
    '''This class is responsible for all the text
        processing like counting frequency etc'''

    def nav_extractor(self, words_list):
        tagged_words = nltk.pos_tag(words_list)
        extracted_words = []
        for word, pos in tagged_words:
            if pos == 'NN' or pos == 'VBD':
                extracted_words.append(word)
        return extracted_words

    def dictionary_generator(self, words_list):
        extracted_words = self.nav_extractor(words_list)
        words_dict = {}
        for word in extracted_words:
            if words_dict.get(word):
                words_dict[word] = words_dict[word] + 1
            else:
                words_dict[word] = 1
        return words_dict
