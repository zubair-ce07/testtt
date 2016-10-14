from urllib.parse import urljoin

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from hitmeister.items import HitmeisterProduct


class HitmeisterSpider(CrawlSpider):
    name = "hitmeister_spider"
    allowed_domains = ['hitmeister.de']
    start_urls = [
        'https://www.hitmeister.de/schuhe/',
        'https://www.hitmeister.de/accessoires/',
        'https://www.hitmeister.de/kleidung/',
    ]
    listings_xpaths = ['//div[@data-name="CategoryTree"]//ul/li',
                       '//div[@data-name="CategoryTree"]//ul/li[@class="level-2 "]',
                       ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_xpaths), follow=True, callback='parse_hitmeister_page'),
        Rule(LinkExtractor(restrict_xpaths=['//ul[@class="pagination list -inline"]/li[last()]']),
             callback='parse_hitmeister_page'),
        Rule(LinkExtractor(restrict_xpaths=['//div[@class ="col-md-9"]//a[contains(@href, "/product")]']),
             callback='parse_hitmeister_products')
    )

    def parse_hitmeister_page(self, response):
        url = self.next_page(response)
        if url:
            page_url = urljoin('https://www.hitmeister.de', url[0])
            yield Request(url=page_url)

    def next_page(self, response):
        return response.xpath('//ul[@class="pagination list -inline"]/li[last()]').extract()

    def parse_hitmeister_products(self, response):
        hitmeister_product = HitmeisterProduct()
        hitmeister_product['url'] = response.url
        hitmeister_product['product_id'] = self.product_id(response)
        hitmeister_product['name'] = self.product_name(response)
        hitmeister_product['price'] = self.product_price(response)
        hitmeister_product['gender'] = self.gender(response)
        hitmeister_product['description'] = self.description(response)
        hitmeister_product['brand'] = self.brand(response)
        hitmeister_product['image_urls'] = self.image_urls(response)
        hitmeister_product['category'] = self.category(response)
        hitmeister_product['color'] = self.product_color(response)
        hitmeister_product['size'] = self.product_size(response)
        yield hitmeister_product

    def product_id(self, response):
        return response.xpath("//div['@data-id-item']/@data-id-item").extract_first()

    def product_name(self, response):
        return response.xpath("//h1/text()").extract_first()

    def product_price(self, response):
        return response.xpath("//span[@itemprop='price']/text()").extract_first()

    def gender(self, response):
        return response.xpath(
            "(//div[text()='Zielgruppen:']/parent::*)/following-sibling::td/a/text()").extract_first()

    def description(self, response):
        return response.xpath("//div[@itemprop='description']/p/text()").extract()

    def brand(self, response):
        return response.xpath("((//div[text()='Hersteller:']/parent::*)/following-sibling::*/descendant::*/text())"
                              "[position()=1]").extract_first()

    def image_urls(self, response):
        return response.xpath("(//@data-src)[position() != 2]").extract()

    def category(self, response):
        return response.xpath("(//span[@itemprop='name'])[position() != last() and  position()!=1]/text()").extract()

    def product_color(self, response):
        return response.xpath(
            "(//div[text()='Farbe:']/parent::*)/following-sibling::td/span/text()").extract_first()

    def product_size(self, response):
        return response.xpath(
            "(//div[text()='Größe:']/parent::*)/following-sibling::td/span/text()").extract_first()
