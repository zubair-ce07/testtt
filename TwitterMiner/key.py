__author__ = 'abdul'

import os


class Keys:
    """
    Class to read and store credential keys
    """

    consumer_key = ""
    consumer_secret_key = ""
    access_key = ""
    access_secret_key = ""

    def __init__(self):
        """
        Reads credential keys read from environment variables
        """
        self.consumer_key = os.environ.get('consumerKey')
        self.consumer_secret_key = os.environ.get('consumerSecretKey')
        self.access_key = os.environ.get('accessToken')
        self.access_secret_key = os.getenv('accessTokenSecret')
