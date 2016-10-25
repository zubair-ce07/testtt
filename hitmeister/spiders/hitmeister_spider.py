import logging
from urllib.parse import urljoin

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from hitmeister.items import HitmeisterProduct


class HitmeisterSpider(CrawlSpider):
    name = "hitmeister_spider"
    allowed_domains = ['hitmeister.de', ]
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
        Rule(LinkExtractor(allow=[r'/category/\d+/p\d+'], restrict_xpaths=['//form[@id="refinement_top_form"]', ]),
             callback='parse_hitmeister_page'),
        Rule(LinkExtractor(restrict_xpaths=['//div[@class ="col-md-9"]//a[contains(@href, "/product")]']),
             callback='parse_hitmeister_products')
    )

    def parse_hitmeister_page(self, response):
        logging.warning(response.url)
        url = self.next_page(response)
        if url:
            page_url = urljoin('https://www.hitmeister.de', url)
            yield Request(url=page_url)

    def next_page(self, response):
        url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        if '/category' in url:
            # find page number increment and return with new page
            url_part = url.split('/')
            page_number = url_part[-2][1:]
            page_number = int(page_number)
            page_number += 1
            url_part[-2] = 'p' + str(page_number)
            return '/category/' + url_part[-3] + '/' + url_part[-2]
        else:
            # find category url and go to second page
            url = response.xpath('//form[@id="refinement_top_form"]/@action').extract_first()
            url = urljoin(url, 'p2/')
            return url

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
