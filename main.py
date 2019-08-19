from scrapy.crawler import CrawlerProcess

import product_spider


def main():
    process = CrawlerProcess({'FEED_FORMAT': 'json', 'FEED_URI': 'products.json', 'CONCURRENT_REQUESTS': 100,
                              'CONCURRENT_REQUESTS_PER_IP': 100})
    process.crawl(product_spider.ProductSpider)
    process.start()


if __name__ == '__main__':
    main()