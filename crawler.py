#!/usr/bin/python
import argparse
import asyncio
from algorithm import Algorithm
# import requests
# import parsel
URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/',
        'http://www.arbisoft.com/']

def main(argv):
    algorithm = Algorithm(URLS, argv.workers, argv.delay, argv.max_urls)
    algorithm.run()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete()
    # loop.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="Website url to crawl")
    parser.add_argument('-w', "--workers", type=int, help="Number of worker threads")
    parser.add_argument('-d', "--delay", type=int, help="Download delay for making two concurrent requests")
    parser.add_argument('-m', "--max-urls", type=int, help="Maximum urls to visit")
    args = parser.parse_args()
    main(args)





# We can use a with statement to ensure threads are cleaned up promptly
