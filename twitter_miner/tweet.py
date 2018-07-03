__author__ = 'abdul'

import classifier

class Tweet:
    text = ""
    category = ""
    classifier = classifier.Classifier()

    def __init__(self, tweet_text):
        self.text = tweet_text
        self.category = self.classifier.classify(self.text)

    def print(self):
        print(self.text)
        print("Category: " + self.category)
