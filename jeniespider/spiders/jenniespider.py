from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spiders.parse import Parse


class JanieSpider(CrawlSpider):
    name = "janiespider"
    parser = Parse()
    allowed_domains = ["janieandjack.com", "i1.adis.ws"]
    start_urls = (
        'http://www.janieandjack.com/',
    )
    rules = (
        Rule(LinkExtractor(
            restrict_css='.desktop-only .subcategory')),
        Rule(LinkExtractor(
            restrict_css='.infinite-scroll-placeholder-down',
            tags=['div'], attrs=['data-grid-url'])
        ),
        Rule(LinkExtractor(restrict_css='.product-image .thumb-link'),
             callback=parser.parse_product),

    )