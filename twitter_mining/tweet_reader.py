import tweepy


class TweetReader:

    def __init__(self):
        self.__CONSUMER_KEY = "os1fm4XImRtiE9fKk9ZbmFp4f"
        self.__CONSUMER_SECRET = \
            "zJHb7lgToonbAS67StM1D5bW6SLLT2OVWBm5zIPibXI1EOlnNZ"
        self.__ACCESS_TOKEN = \
            "872773211934515200-AVLJYY1JfreNnno9WWg72CDiM1IY6dz"
        self.__ACCESS_TOKEN_SECRET = \
            "OTZGdJDnMFeTjPVY7JR8TwxW4AcxyfJWfshJgRzia7xVI"
        self.auth = None
        self.api = None

    def authorize_connection(self):
        self.auth = tweepy.OAuthHandler(self.__CONSUMER_KEY, self.__CONSUMER_SECRET)
        self.auth.set_access_token(self.__ACCESS_TOKEN, self.__ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)

    def read_public_tweets(self):
        public_tweets = self.api.home_timeline()

        for tweet in public_tweets:
            yield tweet.text
        return
