__author__ = 'abdul'
import re
# Reference: https://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python

# used further in the class
regexs = [
{'name': 'Mention', 'regex': re.compile(r"@\w+")},
{'name': 'Link', 'regex': re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")},
{'name': 'Hash Tag', 'regex': re.compile(r"#\w+")}
]


class Classifier:
    """
    Defines regexes to classify strings
    """

    def classify(self, string):
        """
        Returns a category after classifying input string
        """
        accumulated_category = "Text, "

        for regex in regexs:
            if regex['regex'].search(string):
                accumulated_category += regex['name'] + ", "

        return accumulated_category
