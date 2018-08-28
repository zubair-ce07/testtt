import sys
import re


class InputSystem:
    '''This class take care of all the required input validation & parsing'''
    def __init__(self):
        pass

    def get_input(self):
        return input("Enter your desired url: ")

    def validate_url(self, url):
        url_regex = re.compile("http[s]?://(?:[a-zA-Z]" +
                               "|[0-9]|[$-_@.&+]|[!*\(\),]|" +
                               "(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        return re.match(url_regex, url) is not None
