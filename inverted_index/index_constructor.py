__author__ = 'abdul'

import sys

import urllib.error as httpError
import argparse

import inverted_index
import url as url_module  # Reason of renaming is multiple use of keyword url in module


class IndexConstructor:
    inverted_index = inverted_index.InvertedIndex()

    def check_arg(self, args=None):
        """
        Takes arguments as input
        """
        parser = argparse.ArgumentParser(description='Enter urls to '
                                                     'create their '
                                                     'inverted indexes.')
        parser.add_argument('-u', '--urls',
                            help='Comma seperated urls with no space. '
                                 'Enter \'rebuild\' to rebuild on existing data',
                            required='True',
                            type=str)
        results = parser.parse_args(args)
        return (results.urls)

    def process_url(self, urls):
        """
        Verifies and downloads contents of a url
        Parsing is also done here
        """
        for url in urls:
            new_url = url_module.Url(url)
            new_url.verify_url(url)
            new_url.download_and_parse()

    def begin_construction(self, args=None):
        """
        Controller function
        accepts arguments and builds inverted index
        """
        urls = self.check_arg(args).split(',')

        if urls[0] != 'rebuild':
            try:
                self.process_url(urls)
            except ValueError as v:
                print(format(v))

        self.inverted_index.build_inverted_index()
        self.inverted_index.write_inverted_index()

if __name__ == '__main__':
    indexer = IndexConstructor()
    try:
        indexer.begin_construction(sys.argv[1:])
    except (FileNotFoundError, httpError.URLError, httpError.HTTPError,
            httpError.ContentTooShortError) as e:
        print(format(e))
