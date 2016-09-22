from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import SheegoItem

class SheegoSpider(CrawlSpider):
    name = "sheego"
    allowed_domains = ["sheego.de"]
    # start_urls = (
    #     'https://www.sheego.de/damenmode-jacken-maentel/',
    # )
    start_urls = (
        'https://www.sheego.de/sheego-casual-steppweste-rosa_468389298-888154-91p.html',
    )
    # rules = [
    #          # Rule(LinkExtractor(allow="sheego.de/", deny=["sheego.de/\?"],  restrict_css="#content"), follow=True),
    #          Rule(LinkExtractor(allow="sheego.de/", deny=["sheego.de/\?"],  restrict_css=".next.js-next.btn.btn-next"), follow=True),
    #          Rule(LinkExtractor(restrict_css=".product__item"),callback='parse_prodcut', follow=True)
    #         ]

    def parse(self, response):
        self.parse_prodcut(response)

    def parse_prodcut(self, response):
        print("Name", self.parse_name(response))
        print("ID", self.parse_product_id(response))
        print("Sizes", self.parse_sizes(response))
        print("Colors", self.parse_colors(response))
        print("Colors", self.parse_category(response))
        item = SheegoItem()
        item['name'] =self.parse_name(response)
        return item

    def parse_name(self, response):
        return response.css(".at-dv-itemName::text").extract()[0].strip()

    def parse_product_id(self, response):
        return response.css(".at-dv-artNr::text").extract()[0].strip()

    def parse_sizes(self, response):
        return response.css(".js-sizeSelector > div > button::attr(data-noa-size)").extract()

    def parse_colors(self, response):
        return response.css(".color-item::attr(title)").extract()

    def parse_category(self, response):
        return response.css(".breadcrumb > li > strong::text").extract()