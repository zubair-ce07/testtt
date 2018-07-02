__author__ = 'abdul'
import re


class Classifier:
    """
    Defines regexes to classify strings
    """

    mention_regex = re.compile(r"@")
    link_regex = re.compile(r"http")
    hashtag_regex = re.compile(r"#")

    def classify(self, string):
        """
        Returns a category after classifying input string
        """
        if self.link_regex.search(string):
            return "Link"
        elif self.hashtag_regex.search(string):
            return "Hash Tag"
        elif self.mention_regex.search(string):
            return "Mention"
        else:
            return "Text"