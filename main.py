from scrapy.crawler import CrawlerProcess

import khelf_crawler


def main():
    process = CrawlerProcess({'FEED_FORMAT': 'json', 'FEED_URI': 'products.json', 'CONCURRENT_REQUESTS': 100,
                              'CONCURRENT_REQUESTS_PER_IP': 100})
    process.crawl(khelf_crawler.KhelfCrawler)
    process.start()


if __name__ == '__main__':
    main()
