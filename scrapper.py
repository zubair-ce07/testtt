import requests
from parsel import Selector


def filter_invalid_urls(urls):
    urls = [url for url in urls if len(url) > 5]
    return urls


def recursively_extract_html(urls, origin, hits_limit, total_hits=0):
    if urls and total_hits < hits_limit:
        target_link = urls.pop(0)

        if target_link.startswith("//"):
            target_link = "http:" + target_link
        if target_link.startswith("/"):
            target_link = origin + target_link
        response = requests.get(target_link)

        total_hits += 1
        print("Total Hits: %s | %s" % (total_hits, target_link))

        parser = Selector(response.text)

        page_links = parser.xpath("//a/@href").extract()
        urls += filter_invalid_urls(page_links)

        recursively_extract_html(urls, origin, hits_limit, total_hits)


def main():
    origin = "http://sfbay.craigslist.org"
    url = "http://sfbay.craigslist.org/search/eby/jjj"
    hits_limit = 100

    recursively_extract_html([url], origin, hits_limit)

if __name__ == '__main__':
    main()
