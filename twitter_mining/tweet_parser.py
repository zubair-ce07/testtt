import re


class TweetParser:

    def parse(self, tweet):
        hash_tags = re.findall(r'\#\w*', tweet)
        at_tags = re.findall(r'\@\w*', tweet)
        links = re.findall(r'http[s]?://[a-zA-Z0-9_\-\./]*', tweet)

        complete_result = hash_tags + at_tags + links
        return complete_result
