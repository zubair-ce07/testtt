import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from kidsbrandstore.parser import Parser


class BrandStoreSpider(CrawlSpider, Parser):
    name = 'brandstore'
    allowed_domains = ['kidsbrandstore.de']
    start_urls = ['http://kidsbrandstore.de/']
    categories_css = [".paginationControl", "div[id=bottom-types]", "div[id=bottom-brands]"]
    products_css = ".bottom-product-grid"
    gender_pairs = {"jungen": "boys", "mädchen": "girls"}
    rules = (
        Rule(LinkExtractor(deny_extensions=['html'], restrict_css=categories_css)),
        Rule(LinkExtractor(restrict_css=products_css), callback="parse_item"),
        )
