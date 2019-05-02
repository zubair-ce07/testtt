import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import scrapy

from oltre_crawler.items import OltreCrawlerItem


class ParseSpider(scrapy.Spider):
    start_url = 'https://www.oltre.com/it/'
    name = "parse_spider"

    def parse(self, response):
        product = OltreCrawlerItem()
        product['retailer_sku'] = self.retailer_sku(response)
        product['market'] = 'it'
        product['retailer'] = 'oltre-it'
        product['gender'] = 'Women'
        product['brand'] = 'oltre'
        product['name'] = self.product_name(response)
        product['category'] = self.product_category(response)
        product['date'] = str(datetime.datetime.now())
        product['url'] = response.url
        product['description'] = self.product_description(response)
        product['care'] = self.product_care(response)
        product['image_urls'] = self.product_image_urls(response)
        product['spider_name'] = 'oltre_spider'
        product['skus'] = self.skus(response)
        product['requests'] = self.color_requests(response)

        return self.next_request_or_product(product)

    def color_requests(self, response):
        color_urls = response.xpath(
            '(//ul[@class="swatches color"])[1]/li[not(contains(@class,"selectable selected"))]/a/@href').getall()
        return [response.follow(color, callback=self.parse_skus) for color in color_urls]

    def parse_skus(self, response):
        product = response.meta['product']
        product['skus'].append(self.skus(response))

        return self.next_request_or_product(product)

    def next_request_or_product(self, product):
        if not product['requests']:
            del product['requests']
            return product

        request = product['requests'].pop()
        request.meta['product'] = product
        return request

    def product_name(self, response):
        return response.css('.product-name::text').get()

    def retailer_sku(self, response):
        return response.css('#pid::attr(value)').get()

    def product_category(self, response):
        return response.css('.breadcrumb-element ::text').getall()

    def product_description(self, response):
        raw_description = response.xpath('//div[@id="description"]/div/text()').getall()
        description = [description.strip() for description in raw_description]
        return list(filter(None, description))

    def product_care(self, response):
        raw_care = response.css('#wash > div::text').getall()
        care = [care.strip() for care in raw_care]
        return list(filter(None, care))

    def product_image_urls(self, response):
        image_urls = response.css('.product-thumbnails ::attr(href)').getall()
        return [response.urljoin(url) for url in image_urls]

    def product_price_detail(self, response):
        product_price = {
            'price': response.css('.price-sales.gtm-sale::text').get().strip().split('€')[1],
            'currency': 'EUR',
        }
        previous_price = response.xpath('(//span[@class="price-standard"])[1]/text()').getall()
        if previous_price:
            product_price['previous_price'] = list(map(str.strip, previous_price))

        return product_price

    def size_options(self, response):
        size_options = response.xpath('(//ul[@class="swatches size"])[1]/li/a/text()').getall()
        return [size.strip() for size in size_options]

    def skus(self, response):
        product_detail = []
        common_sku = {}
        retailer_sku = self.retailer_sku(response)
        color = response.css('.selected-value::text,.title-variation-color::text ').get()

        for size in self.size_options(response):
            common_sku.update(self.product_price_detail(response))
            common_sku['size'] = size
            common_sku['sku_id'] = retailer_sku + size
            if color:
                common_sku['color'] = color.strip()

            product_detail.append(common_sku)
        return product_detail


class OltreSpider(CrawlSpider):
    name = 'oltre_spider'
    start_urls = ['https://www.oltre.com/it']

    allowed_domains = ['oltre.com']
    parser = ParseSpider()

    category_css = ['.main-menu']
    product_css = ['.product-name',
                   '.page-next'
                   ]
    rules = (
        Rule(LinkExtractor(restrict_css=category_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback=parser.parse)
    )

