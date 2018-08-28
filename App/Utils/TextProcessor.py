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
