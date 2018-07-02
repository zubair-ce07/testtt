__author__ = 'abdul'

import key
import classifier
import tweepy


class Miner:
    """
    Class to mine data from twitter
    """
    keys_obj = key.Keys()
    classifier_obj = classifier.Classifier()

    def mineData(self, message, count):
        """
        Searches and displays 'count' tweets found against 'message'
        """
        auth = tweepy.OAuthHandler(self.keys_obj.consumer_key, self.keys_obj.consumer_secret_key)
        auth.set_access_token(self.keys_obj.access_key, self.keys_obj.access_secret_key)

        api = tweepy.API(auth)
        for tweet in tweepy.Cursor(api.search,
                               q=message,
                               lang="en").items(count):
            print(tweet.text)
            print("Category: " + self.classifier_obj.classify(tweet.text))
            print("----")
            print()
