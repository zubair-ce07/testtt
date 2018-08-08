from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from .product_schema import Parser


class JoopSpider(CrawlSpider):
    name = "joop_de"
    parser = Parser()
    start_urls = [
        'https://joop.com/de/de/'
    ]
    rules = (Rule(LinkExtractor(restrict_css='#products>li>a'), callback="parse_product"),
             Rule(LinkExtractor(restrict_css='#mainnav'), callback='parse'),
             )

    def parse(self, response):
        for request in super(JoopSpider, self).parse(response):
            trail = response.meta.get("trail", []).copy()
            trail.append(response.url)
            request.meta["trail"] = trail
            yield request

    def parse_product(self, response):
        if response.css("body.pda"):
            for url_or_item in self.parser.parse(response):
                if not isinstance(url_or_item, dict):
                    request = response.follow(url_or_item, callback=self.parse_product)
                    request.meta["trail"] = response.meta["trail"].copy()
                    request.meta["trail"].append(response.url)
                    yield request
                else:
                    yield url_or_item
