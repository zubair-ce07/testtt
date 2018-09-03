import re
import argparse


class ArgParser:
    '''This class take care of all the required input validation & parsing'''

    def __init__(self):
        self.regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def input_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('url', help="URL to crawl",
                            type=self.validate_url, nargs='?')
        parser.add_argument('action', choices=['n', 'v'], default='n',
                            help="Select action:\n" +
                            "n----- New Crawl\nv----- View Database")
        args = parser.parse_args()
        return args

    def validate_url(self, url):
        if re.match(self.regex, url):
            return url
        msg = "{0} is not a valid url".format(url)
        raise argparse.ArgumentTypeError(msg)
