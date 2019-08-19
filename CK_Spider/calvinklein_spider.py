from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from calvinklein.spiders.calvinklein_parser import CalvinKleinParser


class CalvinKleinSpider(CrawlSpider):
    name = 'calvinklein_spider'
    allowed_domains = ['www.calvinklein.com.au']
    start_urls = ['http://calvinklein.com.au/']

    listings_css = [
        ".main-navigation.active",
        ".pages"
    ]
    products_css = [".product.name.product-item-name"]

    parse_spider = CalvinKleinParser()

    rules = (
        Rule(LinkExtractor(restrict_css=products_css, deny='by'), callback="parse_item"),
        Rule(LinkExtractor(restrict_css=listings_css, deny='by'), callback="parse")
    )

    def parse(self, response):
        current_trail = self.get_trail(response)
        requests = super(CalvinKleinSpider, self).parse(response)
        return [request.replace(meta={**request.meta, 'trail': current_trail.copy()}) for request in requests]

    def parse_item(self, response):
        return self.parse_spider.parse(response)

    def get_trail(self, response):
        css = "meta[name='title']::attr(content)"
        new_trail = [(response.css(css).get().split("|", 1)[0], response.url)]
        return response.meta.get("trail", []) + new_trail
