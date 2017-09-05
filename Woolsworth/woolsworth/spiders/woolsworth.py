import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from woolsworth.items import Product

color_url = 'http://www.woolworths.co.za/store/fragments/product-common/ww/image-shots.jsp'
size_url = 'http://www.woolworths.co.za/store/fragments/product-common/ww/product-item.jsp'
price_url = 'http://www.woolworths.co.za/store/fragments/product-common/ww/price.jsp'


# utility methods
def clean_list(data):
    temp = []
    for item in data:
        temp.append(item.strip())
    temp = list(filter(None, temp))
    return temp


class WoolsworthSpider(CrawlSpider):
    name = 'woolsworth'
    allowed_domains = ['www.woolworths.co.za']

    start_urls = ['http://www.woolworths.co.za/store/cat']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,"icon--right-dark")]/parent::a')),
        Rule(LinkExtractor(deny='/Food/', restrict_css="a.product-card__details"), callback="parse_product"),)

    def parse_product(self, response):
        product = Product()
        self.url(response, product)
        self.retailer_id(response, product)
        self.product_name(response, product)
        self.brand(response, product)
        self.details(response, product)
        self.care(response, product)
        color_ids = self.create_color_ids(response)
        current_color_id = color_ids.pop()
        product['image_urls'] = []
        product['skus'] = {}
        color_formdata = self.create_color_formdata(product['retailer_id'], current_color_id)
        yield scrapy.FormRequest(color_url, callback=self.parse_sku_images, formdata=color_formdata,
                                 meta=self.create_meta(product=product, color_ids=color_ids,
                                                       current_color_id=current_color_id))

    def parse_sku_images(self, response):
        product = response.meta.get('product')
        color_ids = response.meta.get('color_ids')
        current_color_id = response.meta.get('current_color_id')
        if response.css('a.pdp__thumb'):
            product['image_urls'].append({current_color_id: response.css('a.pdp__thumb img::attr(src)').extract()})
        else:
            product['image_urls'].append({current_color_id: response.css('img.img-responsive::attr(src)').extract()})
        size_formdata = self.create_size_formdata(product['retailer_id'], current_color_id)
        yield scrapy.FormRequest(size_url, callback=self.parse_sku_sizes, formdata=size_formdata,
                                 meta=self.create_meta(product=product, color_ids=color_ids,
                                                       current_color_id=current_color_id))

    def parse_sku_sizes(self, response):
        product = response.meta.get('product')
        color_ids = response.meta.get('color_ids')
        current_color_id = response.meta.get('current_color_id')
        if response.css('a.product-size'):
            sizes = response.css('a.product-size::text').extract()
            size_ids = self.create_size_ids(response)
            for i in range(len(sizes)):
                sku_name = '{}_{}'.format(current_color_id, size_ids[i])
                product['skus'].update(
                    {sku_name: {'color': response.css('strong::text').extract_first().strip(), 'size': sizes[i]}})

            if size_ids:
                current_size_id = size_ids.pop()
                price_formdata = self.create_price_formdata(product['retailer_id'], current_color_id, current_size_id)
                sku_name = '{}_{}'.format(current_color_id, current_size_id)
                yield scrapy.FormRequest(price_url, callback=self.parse_size_prices, formdata=price_formdata,
                                         meta=self.create_meta(product=product, sku_name=sku_name, color_ids=color_ids,
                                                               current_color_id=current_color_id, size_ids=size_ids))
        else:
            sku_name = '{}'.format(current_color_id)
            product['skus'].update(
                {sku_name: {'color': response.css('strong::text').extract_first().strip()}})
            price_formdata = self.create_price_formdata(product['retailer_id'], current_color_id)
            yield scrapy.FormRequest(price_url, callback=self.parse_size_prices, formdata=price_formdata,
                                     meta=self.create_meta(product=product, sku_name=sku_name, color_ids=color_ids,
                                                           current_color_id=current_color_id))

    def parse_size_prices(self, response):
        product = response.meta.get('product')
        sku_name = response.meta.get('sku_name')
        size_ids = response.meta.get('size_ids', None)
        color_ids = response.meta.get('color_ids')
        current_color_id = response.meta.get('current_color_id')
        product['skus'][sku_name].update({'currency': response.css('span.currency::attr(content)').extract_first(),
                                          'price': response.css('span.price::attr(content)').extract_first()})
        if response.css('span.price--original'):
            product['skus'][sku_name].update(
                {'original_price': response.css('span.price--original::text').extract_first()})

        if size_ids:
            current_size_id = size_ids.pop()
            price_formdata = self.create_price_formdata(product['retailer_id'], current_color_id, current_size_id)
            sku_name = '{}_{}'.format(current_color_id, current_size_id)
            yield scrapy.FormRequest(price_url, callback=self.parse_size_prices, formdata=price_formdata,
                                     meta=self.create_meta(product=product, sku_name=sku_name,
                                                           current_color_id=current_color_id, color_ids=color_ids,
                                                           size_ids=size_ids))

        elif color_ids:
            current_color_id = color_ids.pop()
            color_formdata = self.create_color_formdata(product['retailer_id'], current_color_id)
            yield scrapy.FormRequest(color_url, callback=self.parse_sku_images, formdata=color_formdata,
                                     meta=self.create_meta(product=product, color_ids=color_ids,
                                                           current_color_id=current_color_id))
        else:
            yield product

    @staticmethod
    def url(response, product):
        product['url'] = response.url.split(';')[0]

    @staticmethod
    def product_name(response, product):
        product['name'] = response.css('h1::text').extract_first().strip()

    @staticmethod
    def brand(response, product):
        if response.css('meta[itemprop="brand"]::attr(content)').extract_first():
            product['brand'] = response.css('meta[itemprop="brand"]::attr(content)').extract_first().strip()

    @staticmethod
    def retailer_id(response, product):
        product['retailer_id'] = response.css('meta[itemprop="productId"]::attr(content)').extract_first().strip()

    @staticmethod
    def details(response, product):
        details_div = response.css('.accordion__toggle--chrome + div')[0]
        details = []
        if details_div.css('p::text'):
            details.append(clean_list(details_div.css('p ::text').extract()))
        if details_div.css('ul:not([class])'):
            details.append(clean_list(details_div.css('ul:not([class]) ::text').extract()))
        product['details'] = details

    @staticmethod
    def care(response, product):
        if len(response.css('.accordion__toggle--chrome + div')) > 2:
            product['care'] = response.css('.accordion__toggle--chrome + div')[1].css(
                'img::attr(src)').extract_first()

    @staticmethod
    def create_color_ids(response):
        color_ids = []
        if response.css('img.colour::attr(onclick)'):
            colors = response.css('img.colour::attr(onclick)').extract()
            for color_id in colors:
                color_ids.append(re.search(r'(\d+)', color_id).group())
        elif response.css('input#catalogRefIds')[0].css('::attr(value)').extract_first():
            color_ids.append(response.css('input#catalogRefIds')[0].css('::attr(value)').extract_first())
        return color_ids

    @staticmethod
    def create_size_ids(response):
        size_ids = []
        sizes = response.css('a.product-size::attr(onclick)').extract()
        for size_id in sizes:
            size_ids.append(re.search(r',(\d+)', size_id).group(1))
        return size_ids

    @staticmethod
    def create_color_formdata(retailer_id, color_id):
        return {
            'productId': retailer_id,
            'colourSKUId': color_id,
        }

    @staticmethod
    def create_size_formdata(retailer_id, color_id):
        return {
            'productItemId': retailer_id,
            'colourSKUId': color_id,
        }

    @staticmethod
    def create_price_formdata(retailer_id, color_id, size_id=""):
        return {
            'productItemId': retailer_id,
            'colourSKUId': color_id,
            'sizeSKUId': size_id
        }

    @staticmethod
    def create_meta(product=None, sku_name=None, color_ids=None, current_color_id=None, size_ids=None):
        return {'product': product, 'sku_name': sku_name, 'color_ids': color_ids,
                'current_color_id': current_color_id, 'size_ids': size_ids}
