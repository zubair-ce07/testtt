import datetime
from urllib.parse import urljoin

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from oltre_crawler.items import OltreCrawlerItem


class Parser:
    start_url = 'https://www.oltre.com/it/'

    def parse_item(self, response):
        product = self.parse_info(response)
        product['requests'] = self.color_requests(response)

        return self.next_request_or_product(product)

    def parse_info(self, response):
        product = OltreCrawlerItem()
        product['retailer_sku'] = self.retailer_sku(response)
        product['market'] = 'it'
        product['retailer'] = 'oltre'
        product['gender'] = 'Women'
        product['brand'] = 'oltre-it'
        product['name'] = self.product_name(response)
        product['category'] = self.product_category(response)
        product['date'] = str(datetime.datetime.now())
        product['url'] = response.url
        product['description'] = self.product_description(response)
        product['care'] = self.product_care(response)
        product['image_urls'] = self.product_image_urls(response)
        product['spider_name'] = 'oltre_spider'
        product['skus'] = self.skus(response)

        return product

    def color_requests(self, response):
        color_urls = response.xpath('(//ul[@class="swatches color"])[1]/li/a/@href').getall()
        return [response.follow(color, callback=self.parse_skus) for color in color_urls[1:]]

    def parse_skus(self, response):
        product = response.meta['product']
        product['skus'].append(self.skus(response))

        return self.next_request_or_product(product)

    def next_request_or_product(self, product):
        if product['requests']:
            request = product['requests'].pop()
            request.meta['product'] = product
            return request
        else:
            del product['requests']

        return product

    def product_name(self, response):
        return response.css('.product-name::text').get()

    def retailer_sku(self, response):
        return response.css('#pid::attr(value)').get()

    def product_category(self, response):
        return response.css('.breadcrumb a::text,.breadcrumb span::text').getall()

    def product_description(self, response):
        description = response.css('#description > div::text').getall()
        return description[1].strip()

    def product_care(self, response):
        raw_care = response.css('#wash > div::text').getall()
        care = [care.strip() for care in raw_care]
        return list(filter(None, care))

    def product_image_urls(self, response):
        image_urls = response.css('.product-thumbnails a::attr(href)').getall()
        return [urljoin(self.start_url, image) for image in image_urls]

    def product_price_detail(self, response):
        product_price = {
            'price': response.css('.price-sales.gtm-sale::text').get().strip().split('€')[1],
            'currency': 'EUR',
        }
        previous_price = response.css('.price-standard::text').get()
        if previous_price:
            product_price['previous_price'] = previous_price.strip().split('€')[1]

        return product_price

    def size_options(self, response):
        size_options = response.xpath('(//ul[@class="swatches size"])[1]/li/a/text()').getall()
        return [size.strip() for size in size_options]

    def skus(self, response):
        product_detail = []
        retailer_sku = self.retailer_sku(response)
        color = response.css('.selected-value::text,.title-variation-color::text ').get()

        for size in self.size_options(response):
            product = self.product_price_detail(response)
            product['size'] = size
            product['sku_id'] = retailer_sku + size
            if color:
                product['color'] = color.strip()

            product_detail.append(product)
        return product_detail


class OltreSpider(CrawlSpider):
    name = 'oltre_spider'
    start_urls = ['https://www.oltre.com/it/']
    parser = Parser()

    category_css = '.main-menu'
    product_css = '.product-name'

    rules = (
        Rule(LinkExtractor(restrict_css=category_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback=parser.parse_item)
    )
