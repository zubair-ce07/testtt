__author__ = 'abdul'

import urllib.request as http
import re

import parser


class Url:

    def __init__(self, url):
        self.url = url
        self.html_data = None
        self.parser = parser.HtmlParser()

    def download_and_parse(self):
        """
        Downloads html content
        Parses html and writes to file
        """
        with http.urlopen(self.url) as f:
            self.html_data = f.read().decode('utf-8')
            self.parser.feed(self.html_data)

    def verify_url(self, url):
        """
        Uses regexes to verify urls
        Reference: https://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
        """
        link_regex = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")
        if not link_regex.search(url):
            raise ValueError(url + " is not a valid url")
