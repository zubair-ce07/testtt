__author__ = 'abdul'
import re


class Classifier:
    """
    Defines regexes to classify strings
    """
    mention_regex = re.compile(r"@\w+")
    # Reference: https://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
    link_regex = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")
    hashtag_regex = re.compile(r"#")

    regex_value = {
     mention_regex : "Mention",
     link_regex: "Link",
     hashtag_regex : "Hash tag"
    }

    def classify(self, string):
        """
        Returns a category after classifying input string
        """
        accumulated_category = ""

        for key, value in self.regex_value.items():
            if key.search(string):
                accumulated_category += value + ", "

        if not accumulated_category:
            return "Text"
        return accumulated_category