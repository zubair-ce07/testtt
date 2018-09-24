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
        parser.add_argument("-n", action='store_true', help="New Crawl")
        parser.add_argument("-v", action='store_true', help="View DB")
        args = parser.parse_args()
        return args

    def validate_url(self, url):

        if re.match(self.regex, url):
            return url
            
        msg = f"{url} is not a valid url"
        raise argparse.ArgumentTypeError(msg)
