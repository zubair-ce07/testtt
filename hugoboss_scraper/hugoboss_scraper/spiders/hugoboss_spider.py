from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from .product_schema import Parser


class HugoBossSpider(CrawlSpider):
    name = "hugo_boss"
    parser = Parser()
    start_urls = [
        'https://www.hugoboss.com/us/'
    ]
    rules = (Rule(LinkExtractor(restrict_css='.swatch-list'), callback="parse_product"),
             Rule(LinkExtractor(restrict_css=('.main-nav__scroller', 'pagingbar__item')), callback='parse'),
             )

    def parse(self, response):
        for request in super(HugoBossSpider, self).parse(response):
            if response.meta.get("trail"):
                trail = response.meta["trail"].copy()
                trail.append(response.url)
                request.meta["trail"] = trail
            else:
                request.meta["trail"] = [response.url]
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
