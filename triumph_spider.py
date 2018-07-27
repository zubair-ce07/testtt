import json
import re
from urllib.parse import urlparse
from urllib.parse import urljoin

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from triumph.items import ProductItem


class ProductsSpider(CrawlSpider):
    name = 'triumph'
    currency = 'GBP'
    deny_urls = ['my-account', 'on/demandware.store\w*', 'sale', 'collections', 'new',
                 '\w*findtheone\w*']
    start_urls = ['http://uk.triumph.com/']

    def process_product_url(url):
        url = urlparse(url)
        return urljoin(ProductsSpider.start_urls[0], url.path)

    rules = (
        Rule(LinkExtractor(restrict_css='.mainLink', deny=deny_urls), callback=None),
        Rule(LinkExtractor(restrict_css='.listItem>.product>.productname>.name>a.productClick',
                           process_value=process_product_url), callback='parse_product'),
        Rule(LinkExtractor(restrict_css='.pagination-wrapper .paginationlink:not(.disabled)',
                           deny='\w*format=ajax'), callback=None),

    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse_product(self, response):

        product_item = ProductItem()
        product_item['retailer_sku'] = self.get_retailer_sku(response)
        product_item['image_urls'] = self.get_image_urls(response)
        product_item['description'] = self.get_description(response)
        product_item['name'] = self.get_product_name(response)

        product_item['gender'] = self.get_gender(response)
        product_item['category'] = self.get_categories(response)
        product_item['url'] = self.get_product_url(response)
        product_item['brand'] = self.get_brand(response)
        product_item['care'] = self.get_product_care(response)

        yield from self.get_skus(response, product_item)

    @staticmethod
    def get_product_name(response):
        return response.css('.product_name::text').extract_first()

    @staticmethod
    def get_product_care(response):
        return response.css('#product_care .care .careimage>div::attr(title)').extract()

    @staticmethod
    def get_description(response):
        return list(filter(None, list(map(str.strip, response
                                          .css('#product_information_features .description')
                                          .xpath('.//text()').extract()))))

    @staticmethod
    def get_retailer_sku(response):
        return response.css('#product_information_features span.productid::text').extract_first()

    @staticmethod
    def get_image_urls(response):
        return response.css('#product_images .mainimage::attr(src)').extract()

    @staticmethod
    def get_gender(response):
        if any("Men" in s for s in ProductsSpider.get_categories(response)):
            return "Men"
        return "Women"

    @staticmethod
    def get_brand(response):
        return response.css(
            '.product_addtocart #form_addtocartbutton::attr(data-gtm-brand)').extract_first()

    @staticmethod
    def get_product_url(response):
        return response.url

    @staticmethod
    def get_categories(response):
        script_sel = response.xpath('//script[contains(.,"var dataParam")]').extract_first()
        product_details = re.findall('\s*var\s*dataParam\s*=(.+?);', script_sel)
        product_details = json.loads(product_details[0])
        return product_details['googletagmanager']['data']['productCategory']

    @staticmethod
    def make_skus(response, query, out_of_stock=False):
        product_skus = []
        color = response.css('.colorswatches_inner li.selected a::attr(title)').extract_first()
        price = response.css('.pricing .price-box>.standardprice::text')
        if not price:
            price = response.css('.pricing .price-box>.salesprice::text')
        previous_prices = response.css('.pricing .price-box>.standardprice.disabled::text')
        previous_prices = [previous_prices.extract_first().strip()[1:] if previous_prices else None]
        product_sizes = list(set(map(str.strip, response.css(query).extract())))
        for size in product_sizes:
            sku = {"colour": color, "price": price.extract_first().strip()[1:],
                   "currency": ProductsSpider.currency, "size": size, "previous_prices": previous_prices}
            if out_of_stock:
                sku["out_of_stock"] = True

            sku["sku_id"] = "{}_{}".format(color, size)
            product_skus.append(sku)
        return product_skus

    @staticmethod
    def get_skus(response, product_item):
        product_item['skus'] = ProductsSpider.parse_skus(response)
        color_urls = [url for url in response.css('.colorswatches_inner'
                                                  ' li:not(.selected) a::attr(href)').extract()
                      if re.match('.*\/Product-ShowProductDetails\?.*', url)]
        for url in color_urls:
            url = urljoin('http://uk.triumph.com/', url)
            yield scrapy.Request(url, callback=ProductsSpider.parse_colors, meta={'item': product_item})

    @staticmethod
    def parse_colors(response):
        product_item = response.meta.get('item')
        product_item['skus'] = product_item.get('skus', []) + ProductsSpider.parse_skus(response)
        return product_item

    @staticmethod
    def parse_skus(response):
        return ProductsSpider.make_skus(response, '#product_variant_details .colorsizes_inner >'
                                                  ' .overlaysizes  a::text') + \
               ProductsSpider.make_skus(response, '#product_variant_details .colorsizes_inner > '
                                                  '.overlaysizes li.disabletile a::text', True)
