from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule

from dawn_scraper.items import DawnScraperItem


class DawnSpider(CrawlSpider):
    name = 'dawn'
    start_urls = ['https://www.dawn.com']
    allowed_domains = ['dawn.com']
    rules = (
        Rule(LinkExtractor(restrict_css='.nav__item')),
        Rule(LinkExtractor(restrict_css='.media__item'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = DawnScraperItem()

        item['content'] = self.get_content(response)
        if not item['content']:
            return
        item['title'] = response.css("meta[property='og:title']::attr(content)").extract_first()
        item['publisher'] = "Dawn.com"
        item['pub_date'] = response.css("meta[property='article:published_time']::attr(content)").extract_first()
        item['image_url'] = response.css("meta[property='og:image']::attr(content)").extract_first()
        item['url'] = response.url
        yield item

    def get_content(self, response):
        raw_content = response.css(".story__content *::text").extract()
        content = [content.strip() for content in raw_content if content.strip()]
        return ' '.join(content)