from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WefashionDeCrawlSpider(CrawlSpider):
    name = 'wefashion-de-crawl'
    allowed_domains = ['example.com']
    start_urls = [
        'http://www.wefashion.de/'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=['.header-top-level-menu', '#category-level-0']), follow=True, callback='parse_category_page'),
    )

    def parse_category_page(self, response):
        print(f"Category {response.url}")
