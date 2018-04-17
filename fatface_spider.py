import json
import re
from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from fatface_scrapy.items import Product


class FatFaceSpider(CrawlSpider):

    name = "fatface"
    allowed_domains = ['fatface.com', 'i1.adis.ws']
    start_urls = ['https://www.fatface.com']
    ids_seen = []

    deny_re = ['blog', 'competition']

    listings_css = "a.b-main-menu__link"
    products_css = "a.b-product-image__link, a.b-product-name__link"

    gender_map = ([
        ('girls', 'girls'),
        ('boys', 'boys'),
        ('women', 'women'),
        ('men', 'men'),
        ('kids', 'unisex-kids')
    ])

    rules = (
        Rule(LinkExtractor(
            restrict_css=listings_css,
            deny=deny_re),
             callback='parse_pagination',
             follow=True
            ),
        Rule(LinkExtractor(
            restrict_css=products_css,
            deny=deny_re),
             callback='parse_product'
            ),
    )

    def parse_pagination(self, response):
        total_products = response.css('div.b-products-counter::text').re_first(r'(\d+) ')

        if not total_products:
            return

        total_products = int(total_products)
        products_per_page = 24
        starting = 0

        if total_products <= products_per_page:
            return

        while total_products > starting:
            products_page = response.urljoin('?start={}'.format(starting))
            yield Request(products_page, callback=self.parse)
            starting += products_per_page

    def parse_product(self, response):

        retailer_sku = self.product_retailer_sku(response)
        if retailer_sku in self.ids_seen:
            return

        self.ids_seen.append(retailer_sku)
        product = Product()
        product['retailer_sku'] = retailer_sku
        product['category'] = self.product_category(response)
        product['gender'] = self.product_gender(product['category'])
        product['brand'] = self.product_brand()
        product['url'] = response.url.split('?')[0]
        product['name'] = self.product_name(response)
        product['description'] = self.product_description(response)
        product['care'] = self.product_care(response)
        product['skus'] = self.product_skus(response)
        product['image_urls'] = []

        images_queue = []
        img_req = Request(self.product_images_link(response), callback=self.parse_images)
        images_queue.append(img_req)

        additional_color_urls = response.css('a.b-variation__link.color::attr(href)').extract()

        if additional_color_urls:
            sku_request = Request(additional_color_urls.pop(0), callback=self.parse_skus)
            sku_request.meta['product'] = product
            request_queue = []
            for color_url in additional_color_urls:
                sku_req = Request(color_url, callback=self.parse_skus)
                request_queue.append(sku_req)
            sku_request.meta['request_queue'] = request_queue
            sku_request.meta['images_queue'] = images_queue
            yield sku_request
        else:
            img_request = images_queue.pop(0)
            img_request.meta['product'] = product
            img_request.meta['images_queue'] = images_queue
            yield img_request

    def parse_skus(self, response):
        product = response.meta['product']
        product['skus'] += self.product_skus(response)

        request_queue = response.meta['request_queue']
        images_queue = response.meta['images_queue']
        img_req = Request(self.product_images_link(response), callback=self.parse_images)
        images_queue.append(img_req)

        if request_queue:
            sku_request = request_queue.pop(0)
            sku_request.meta['product'] = product
            sku_request.meta['request_queue'] = request_queue
            sku_request.meta['images_queue'] = images_queue
            yield sku_request
        else:
            img_request = images_queue.pop(0)
            img_request.meta['product'] = product
            img_request.meta['images_queue'] = images_queue
            yield img_request

    def parse_images(self, response):
        product = response.meta['product']
        product['image_urls'] += self.product_images(response)

        images_queue = response.meta['images_queue']

        if images_queue:
            img_request = images_queue.pop(0)
            img_request.meta['product'] = product
            img_request.meta['images_queue'] = images_queue
            yield img_request
        else:
            yield product

    @staticmethod
    def product_images_link(response):
        return response.css('ul.b-product-preview::attr(data-imageset)').extract_first()

    @staticmethod
    def product_images(response):
        images = json.loads(response.text)
        image_urls = []
        for image in images['items']:
            image_urls.append(image['src'])
        return image_urls

    @staticmethod
    def product_retailer_sku(response):
        retailer_sku = response.css('p.b-content-upc::text').re_first(r'Product code: (\d+)')
        return clean(retailer_sku)

    @staticmethod
    def product_category(response):
        category = clean(response.css('span[itemprop="name"]::text').extract())
        if category[0] == 'Home':
            category = category[1:]
        return category

    def product_gender(self, categories):
        for gender_key, gender_value in self.gender_map:
            for category in categories:
                if gender_key in category.lower():
                    return gender_value
        return 'unisex-adults'

    @staticmethod
    def product_brand():
        return 'FatFace'

    @staticmethod
    def product_name(response):
        name = response.css('h1.b-product-title ::text').extract_first()
        return clean(name)

    @staticmethod
    def product_description(response):
        desc_css = ('.b-product-short-description::text, .b-product-promo__message::text, '
                    '.b-content-longdesc::text, .b-content-bullets ::text')
        desc = response.css(desc_css).extract()
        return clean(desc)

    @staticmethod
    def product_care(response):
        care = response.css('section.b-content-care li::text').extract()
        return clean(care)

    @staticmethod
    def product_price(response):
        price = response.css('span.b-price__digit ::text').re(r'(\d+)')
        price = int(float('.'.join(price))*100)
        return price

    @staticmethod
    def product_colour(response):
        colour = response.css('span.b-product-variations__value ::text').extract_first()
        return clean(colour)

    @staticmethod
    def product_currency(response):
        currency = response.css('script ::text').re_first(r'"currencyCode":"(\w+)"')
        return clean(currency)

    def product_skus(self, response):
        sizes = response.css('ul.b-variation__list.size li')
        skus = []
        for size in sizes:
            sku = {}
            sku['price'] = self.product_price(response)
            sku['currency'] = self.product_currency(response)
            sku['colour'] = self.product_colour(response)
            sku['size'] = size.css('span::text').extract_first()
            if size.css('.unselectable'):
                sku['out_of_stock'] = True
            sku['sku_id'] = '{}_{}'.format(sku['colour'], sku['size'])
            skus.append(sku)
        return skus


def clean(formatted):
    if not formatted:
        return formatted
    if isinstance(formatted, list):
        cleaned = [re.sub(r'\s+', ' ', each).strip() for each in formatted]
        return list(filter(None, cleaned))
    return re.sub(r'\s+', ' ', formatted).strip()
