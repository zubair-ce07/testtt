from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from piazza.spiders.piazza_product import ProductParser


class PiazzaSpider(CrawlSpider):
    name = "piazza-crawl"
    start_urls = [
        'https://www.piazzaitalia.it/',
    ]
    custom_settings = {
        'REDIRECT_ENABLED': True,
    }
    handle_httpstatus_all = True

    rules = (
        Rule(LinkExtractor(restrict_css=('.item.pages-item-next > a', '.level-top', '.level1 > a'))),

        Rule(LinkExtractor(restrict_css=('.product-item-link',)), callback='parse_product'),
    )

    # def parse_(self, response):
    #     # req = Request(response.url, callback=self.parse)
    #     # # req = super(CrawlSpider, self).parse(response)
    #     # req.meta['trail'] = response.url
    #     # return req
    #     # # return req
    #     # # return super(CrawlSpider, self).parse(req)
    #     # # return response.follow(req, callback=self.parse)
    #     yield Request(response.url, meta={'trail': response.url})

    @staticmethod
    def parse_product(response):
        return ProductParser().parse(response)
