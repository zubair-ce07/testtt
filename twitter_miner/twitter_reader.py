__author__ = 'abdul'

import tweepy
import tweet
import os


class TwitterReader:
    """
    Class to mine data from twitter
    """
    consumer_key = ""
    consumer_secret_key = ""
    access_key = ""
    access_secret_key = ""

    twitter_api = None
    tweets = []

    def __init__(self):
        """
        Reads credential keys read from environment variables
        """
        self.consumer_key = os.environ.get('consumerKey')
        self.consumer_secret_key = os.environ.get('consumerSecretKey')
        self.access_key = os.environ.get('accessToken')
        self.access_secret_key = os.getenv('accessTokenSecret')

        if None in (self.consumer_key, self.consumer_secret_key,
                    self.access_key,self.access_secret_key):
            raise ValueError('Environment variables not found')

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret_key)
        auth.set_access_token(self.access_key, self.access_secret_key)

        self.twitter_api = tweepy.API(auth)

    def read_tweets(self, search_string, number_of_tweets):
        """
        Searches and displays 'count' tweets found against 'message'
        """
        for unit_tweet in tweepy.Cursor(self.twitter_api.search,
                               q=search_string,
                               lang="en").items(number_of_tweets):
            new_tweet = tweet.Tweet(unit_tweet.text)
            self.tweets.append(new_tweet)
        return self.tweets
