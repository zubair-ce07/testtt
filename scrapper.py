import requests
from parsel import Selector
import pdb


def recursively_extract_html(urls, hits_limit, total_hits = 0):
    if urls and total_hits <= hits_limit:
        target_link = urls[0]
        response = requests.get(target_link)
        total_hits += 1

        parser = Selector(response.text)
        page_links = parser.css("body a")

        recursively_extract_html(page_links, hits_limit, total_hits)


def main():
    url = "http://stackoverflow.com/"
    hits_limit = 100

    recursively_extract_html([url], hits_limit)

if __name__ == '__main__':
    main()
