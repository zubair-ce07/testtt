import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews, stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import pickle


class SentimentalClassifier():
    def __init__(self):
        self.train_set = None
        self.test_set = None
        self.classifier = None
        self.split_ratio = 0.75

    def __create_word_features(self, words):
        stemmer = SnowballStemmer('english')

        useful_words = [stemmer.stem(word.lower()) for word in words
                        if word.isalpha() and word.lower()
                        not in stopwords.words("english")]

        my_dict = dict([(word, True) for word in useful_words])
        return my_dict

    def __get_features_for_category(self, category):
        features = []
        for fileid in movie_reviews.fileids(category):
            words = movie_reviews.words(fileid)
            features.append((self.__create_word_features(words), category))
        return features

    def classify(self, text):
        if self.classifier:
            return self.classifier.classify(self.__create_word_features(word_tokenize(text)))
        return None

    def load_data(self):
        positive_documents = self.__get_features_for_category('pos')
        negative_documents = self.__get_features_for_category('neg')

        negative_split = int(len(negative_documents) * self.split_ratio)
        positive_split = int(len(positive_documents) * self.split_ratio)

        self.train_set = negative_documents[:negative_split] + positive_documents[:positive_split]
        self.test_set = negative_documents[negative_split:] + positive_documents[positive_split:]

    def train(self):
        self.classifier = NaiveBayesClassifier.train(self.train_set)

    def load_classifier(self, name):
        try:
            (self.classifier, self.train_set, self.test_set, self.split_ratio) = pickle.load(open(name, 'rb'))
        except FileNotFoundError:
            raise

    def save_classifier(self, name):
        if self.classifier:
            data = (self.classifier, self.train_set, self.test_set, self.split_ratio)
            pickle.dump(data, open(name, 'wb'))
            return True
        return False

    def calculate_accuracy(self, train_set=False):
        test_set = self.test_set
        if train_set:
            test_set = self.train_set
        if test_set and self.classifier:
            return nltk.classify.util.accuracy(self.classifier, test_set) * 100
        return None