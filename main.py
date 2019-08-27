from scrapy.crawler import CrawlerProcess

import journelle_crawler


def main():
    process = CrawlerProcess({'FEED_FORMAT': 'json', 'FEED_URI': 'products.json', 'CONCURRENT_REQUESTS': 10,
                              'CONCURRENT_REQUESTS_PER_IP': 10})
    process.crawl(journelle_crawler.JournelleCrawler)
    process.start()


if __name__ == '__main__':
    main()
