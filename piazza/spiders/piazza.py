from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from piazza.spiders.piazza_product import ProductParser


class PiazzaSpider(CrawlSpider):
    name = "piazza-crawl"
    start_urls = [
        'https://www.piazzaitalia.it/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=('.item.pages-item-next > a', '.level-top', '.level1 > a')), callback='parse'),

        Rule(LinkExtractor(restrict_css=('.product-item-link',)), callback='parse_product'),
    )

    product_parser = ProductParser()

    def parse(self, response):
        requests = super().parse(response)
        for req in requests:
            if 'trail' in req.meta.keys():
                req.meta['trail'] = req.meta['trail'].append(response.url)
            else:
                req.meta['trail'] = [response.url]
            yield req

    def parse_product(self, response):
        return self.product_parser.parse(response)
