from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spiders.parse import Parser
from spiders.mixin import Mixin


class JanieSpider(CrawlSpider, Mixin):
    name = "janiespider"
    parser = Parser()
    rules = (
        Rule(LinkExtractor(
            restrict_css='.desktop-only .subcategory')),
        Rule(LinkExtractor(
            restrict_css='.infinite-scroll-placeholder-down',
            tags=['div'], attrs=['data-grid-url'])
        ),
        Rule(LinkExtractor(restrict_css='.product-image .thumb-link'),
             callback=parser.parse),

    )
