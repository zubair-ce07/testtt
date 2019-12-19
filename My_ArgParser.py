from argparse import ArgumentParser
import sys
import os


class My_ArgParser(ArgumentParser):

    def __init__(self):
        super().__init__(description='Task 2 Crawler')
        self.my_add_args()
        self.args = self.parse_args(sys.argv)

    def my_add_args(self):

        self.add_argument(
            'file_name',
            help='name of file'
        )

        self.add_argument(
            'crawler_type',
            type=int,
            help='1 for parallel crawler 2 for async crawler'
        )

        self.add_argument(
            'base_URL',
            type=str,
            help='base url to crawl'
        )

        self.add_argument(
            '-d',
            action='store',
            type=int,
            help='Download Delay in Seconds',
            default=0
        )

        self.add_argument(
            '-m',
            action='store',
            type=int,
            help='Max pages to crawl',
            default=200
        )

        self.add_argument(
            '-r',
            action='store',
            type=int,
            help='Number of request',
            default=4
        )

# /usr/bin/python3.6 "/home/waleed/Desktop/Task 2/main.py" 1 http://quotes.toscrape.com/ -d 0 -m 200 -r 4
#main.py 1 http: // quotes.toscrape.com / -d 0 - m 200 - r 4
