from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from rebellious.rebellious_parse_spider import RebelliousParseSpider


class RebelliousCrawler(CrawlSpider):
    name = 'rebellious_crawler'
    allowed_domains = ['rebelliousfashion.co.uk']
    start_urls = ['http://rebelliousfashion.co.uk/?___store=usd']
    listings_css = ['#nav ul.level0', '.next']
    product_css = '.products-grid'
    allow_r = '.html$'
    product_parser = RebelliousParseSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=(listings_css)), callback='parse'),
        Rule(LinkExtractor(restrict_css=(product_css), allow=(allow_r)),
             callback=product_parser.parse_product),
    )
