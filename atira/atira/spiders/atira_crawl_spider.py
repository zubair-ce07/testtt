from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from atira.spiders.atira_parse_spider import AtiraParseSpider

class AtiraCrawlSpider(CrawlSpider):
    name = "atira"
    allowed_domains =['atira.com']
    start_urls = ['https://atira.com/']

    special_offers = ['a:contains("Offer") ']
    listings_css = ['.ubermenu-item-level-2 .ubermenu-target-with-image']

    rules = (
        Rule(LinkExtractor(restrict_css=special_offers), callback='parse_deal'),
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_item')
    )

    item_parser = AtiraParseSpider()
    deals = None

    def parse_deal(self, response):
        css = '.content-content p:first-of-type ::text'
        self.deals = response.css(css).extract()

    def parse_item(self, response):
        response.meta['deals'] = self.deals
        return self.item_parser.parse(response)
