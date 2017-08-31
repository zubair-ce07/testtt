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
    return temp


def create_color_ids(response):
    color_ids = []
    color_funcs = response.css('img.colour::attr(onclick)').extract()
    for color_id in color_funcs:
        color_ids.append(re.search(r'(\d+)', color_id).group())
    return color_ids


def create_size_ids(response):
    size_ids = []
    size_funcs = response.css('a.product-size::attr(onclick)').extract()
    for size_id in size_funcs:
        size_ids.append(re.search(r',(\d+)', size_id).group(1))
    return size_ids


class WoolsworthSpider(CrawlSpider):
    name = 'woolsworth'
    allowed_domains = ['www.woolworths.co.za']

    # start_urls = [
    #     'http://www.woolworths.co.za/store/cat/Kids/_/N-1z13s2t']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//span[@class="icon icon--right-dark"]/parent::a')),
        Rule(LinkExtractor(
            restrict_css="a.product-card__details"), callback="parse_product"),)

    def start_requests(self):
        start_urls = [
            'http://www.woolworths.co.za/store/prod/Gifts/Gifts-for-Him/Underwear-Socks/AKJP-Print-Socks/_/A-503821762', ]
        # 'http://www.woolworths.co.za/store/prod/Women/Clothing/New-Arrivals/Metallic-Textured-Slip-Dress/_/A-503949756',
        # 'http://www.woolworths.co.za/store/prod/Kids/Boys/Underwear-Socks/Batman-Socks-3-Pack/_/A-503555910',
        # 'http://www.woolworths.co.za/store/prod/Kids/Boys/Tops-Tees/Lightning-Knit/_/A-503777870',
        # 'http://www.woolworths.co.za/store/prod/Kids/Boys/Bottoms/Adjustable-Bermuda-Shorts/_/A-503771730',
        # 'http://www.woolworths.co.za/store/prod/Men/Clothing/Shirts/Broad-Stripe-Cotton-Shirt/_/A-503743208']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        product = Product()
        self.url(response, product)
        self.retailer_id(response, product)
        self.product_name(response, product)
        self.brand(response, product)
        self.details(response, product)
        self.care(response, product)
        color_ids = create_color_ids(response)
        current_color_id = color_ids.pop()
        product['image_urls'] = []
        product['skus'] = {}
        color_formdata = {
            'productId': product['retailer_id'],
            'colourSKUId': current_color_id,
        }
        size_formdata = {
            'productItemId': product['retailer_id'],
            'colourSKUId': current_color_id,
        }
        # yield scrapy.FormRequest(size_url, callback=self.parse_sku_sizes, formdata=size_formdata,
        #                          meta={'product': product, 'color_ids': color_ids,
        #                                'current_color_id': current_color_id})
        yield scrapy.FormRequest(color_url, callback=self.parse_sku_images, formdata=color_formdata,
                                 meta={'product': product, 'color_ids': color_ids,
                                       'current_color_id': current_color_id})

    def parse_sku_images(self, response):
        product = response.meta.get('product')
        color_ids = response.meta.get('color_ids')
        current_color_id = response.meta.get('current_color_id')
        product['image_urls'].append({current_color_id: response.css('a.pdp__thumb img::attr(src)').extract()})
        size_formdata = {
            'productItemId': product['retailer_id'],
            'colourSKUId': current_color_id,
        }
        yield scrapy.FormRequest(size_url, callback=self.parse_sku_sizes, formdata=size_formdata,
                                 meta={'product': product, 'color_ids': color_ids,
                                       'current_color_id': current_color_id})
    def parse_sku_sizes(self, response):
        product = response.meta.get('product')
        color_ids = response.meta.get('color_ids')
        current_color_id = response.meta.get('current_color_id')
        if response.css('a.product-size'):
            sizes = response.css('a.product-size::text').extract()
            size_ids = create_size_ids(response)
            for i in range(len(sizes)):
                sku_name = '{}_{}'.format(current_color_id, size_ids[i])
                product['skus'].update(
                    {sku_name: {'color': response.css('strong::text').extract_first().strip(), 'size': sizes[i]}})

            if size_ids:
                current_size_id = size_ids.pop()
                price_formdata = {
                    'productItemId': product['retailer_id'],
                    'colourSKUId': current_color_id,
                    'sizeSKUId': current_size_id
                }
                sku_name = '{}_{}'.format(current_color_id, current_size_id)
                yield scrapy.FormRequest(price_url, callback=self.parse_size_prices, formdata=price_formdata,
                                         meta={'product': product, 'sku_name': sku_name, 'color_ids': color_ids,
                                               'current_color_id': current_color_id, 'size_ids': size_ids})
        else:
            sku_name = '{}'.format(current_color_id)
            product['skus'].update(
                {sku_name: {'color': response.css('strong::text').extract_first().strip()}})
            price_formdata = {
                'productItemId': product['retailer_id'],
                'colourSKUId': current_color_id,
            }
            yield scrapy.FormRequest(price_url, callback=self.parse_size_prices, formdata=price_formdata,
                                     meta={'product': product, 'sku_name': sku_name, 'color_ids': color_ids,
                                           'current_color_id': current_color_id})
            # if color_ids:
            #     current_color_id = color_ids.pop()
            #     formdata = {
            #         'productId': product['retailer_id'],
            #         'colourSKUId': current_color_id,
            #     }
            #     yield scrapy.FormRequest(color_url, callback=self.parse_sku_images, formdata=formdata,
            #                              meta={'product': product, 'color_ids': color_ids,
            #                                    'current_color_id': current_color_id})
            # else:
            #     yield product

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
            price_formdata = {
                'productItemId': product['retailer_id'],
                'colourSKUId': current_color_id,
                'sizeSKUId': current_size_id
            }
            sku_name = '{}_{}'.format(current_color_id, current_size_id)
            yield scrapy.FormRequest(price_url, callback=self.parse_size_prices, formdata=price_formdata,
                                     meta={'product': product, 'sku_name': sku_name,
                                           'current_color_id': current_color_id, 'color_ids': color_ids,
                                           'size_ids': size_ids})
        elif color_ids:
            current_color_id = color_ids.pop()
            color_formdata = {
                'productId': product['retailer_id'],
                'colourSKUId': current_color_id,
            }
            yield scrapy.FormRequest(color_url, callback=self.parse_sku_images, formdata=color_formdata,
                                     meta={'product': product, 'color_ids': color_ids,
                                           'current_color_id': current_color_id})
        else:
            yield product


        # if color_ids:
        #     current_color_id = color_ids.pop()
        #     formdata = {
        #         'productId': product['retailer_id'],
        #         'colourSKUId': current_color_id,
        #     }
        #     yield scrapy.FormRequest(color_url, callback=self.parse_sku_images, formdata=formdata,
        #                              meta={'product': product, 'color_ids': color_ids,
        #                                    'current_color_id': current_color_id})
        # else:
        #     yield product

    # def parse_sku(self, response):
    #     product = response.meta.get('product')
    #     color_ids = response.meta.get('color_ids')
    #     if color_ids:
    #         yield scrapy.FormRequest(color_url, callback=self.parse_sku_images,
    #                                  meta={'product': product, 'color_ids': color_ids})



    @staticmethod
    def url(response, product):
        product['url'] = response.url

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
        details_div = response.css('h4.accordion__toggle--chrome + div')[0]
        details = []
        if details_div.css('p::text'):
            details.append(details_div.css('p::text').extract_first().strip())
        if details_div.css('ul:not([class])'):
            details.append(clean_list(details_div.css('ul:not([class]) li::text').extract()))
        product['details'] = details

    @staticmethod
    def care(response, product):
        if len(response.css('h4.accordion__toggle--chrome + div')) > 2:
            product['care'] = response.css('h4.accordion__toggle--chrome + div')[1].css(
                'img::attr(src)').extract_first()
