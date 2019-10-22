import json
import re
import scrapy

from scrapy import Selector
from scrapy.spiders import CrawlSpider

from ..items import WhiteStuffItem


class WhiteStuffParser:

    def parse_details(self, response):
        whitestuff_product = WhiteStuffItem()
        whitestuff_product['retailer_sku'] = self.extract_retailor_sku(response)
        whitestuff_product['gender'] = self.extract_gender(response)
        whitestuff_product['category'] = self.extract_category(response)
        whitestuff_product['brand'] = self.extract_brand()
        whitestuff_product['url'] = self.extract_url(response)
        whitestuff_product['name'] = self.extract_name(response)
        whitestuff_product['description'] = self.extract_description(response)
        whitestuff_product['care'] = self.extract_care(response)

        yield self.extract_skus_requests(response, whitestuff_product)

    def extract_skus_requests(self, response, whitestuff_product):
        master_sku = response.css('::attr(data-variation-master-sku)').get()
        json_url = 'https://www.whitestuff.com/action/GetProductData-FormatProduct?Format=JSON&ReturnVariable=true&'
        json_url += 'ProductID=' + master_sku
        return scrapy.Request(json_url, callback=self.extract_skus, meta={'item': whitestuff_product})

    def extract_retailor_sku(self, response):
        return response.css('[itemprop="sku"]::text').get()

    def extract_gender(self, response):
        return response.css('.breadcrumb-list__item a::text').getall()[1]

    def extract_category(self, response):
        return self.clean(response.css('.breadcrumb-list__item a::text').getall())

    def extract_brand(self):
        return 'WhiteStuff'

    def extract_url(self, response):
        return response.url

    def extract_name(self, response):
        return self.clean(response.css('[itemprop="name"]::text').get())

    def extract_description(self, response):
        return self.clean(response.css('.js-lineclamp::text').getall())

    def extract_care(self, response):
        return response.css('.ish-productAttributes ::text').getall()

    def extract_imgs_urls(self, images_dict):
        return [image['src'] for image in images_dict]

    def extract_skus(self, response):
        whitestuff_product = response.meta['item']
        product_info = \
            json.loads(response.body_as_unicode()[response.body_as_unicode().find('{'):-1])['productVariations']
        whitestuff_product['img_urls'] = []
        whitestuff_product['skus'] = []

        for product in product_info.values():
            sku = {'color': product['colour']}
            sku['size'] = product['size']
            sku['previous_price'] = product['listPrice']
            sku['price'] = product['salePrice']
            sku['out_of_stock'] = not product['inStock']
            sku['sku_id']: sku['color'] + '_' + sku['size']
            whitestuff_product['img_urls'] += self.extract_imgs_urls(product['images'])
            whitestuff_product['skus'].append(sku)

        yield whitestuff_product

    def clean(self, list_to_strip):
        if isinstance(list_to_strip, basestring):
            return list_to_strip.strip()
        return [str_to_strip.strip() for str_to_strip in list_to_strip if str_to_strip.strip()]


class WhiteStuffSpider(CrawlSpider):
    name = 'whitestuff'
    start_urls = [
        'https://www.whitestuff.com/',
    ]

    def parse(self, response):
        top_categories_sel = response.css('.navbar__item')[:4]
        for top_category_sel in top_categories_sel:
            top_menu_id = top_category_sel.css('::attr(data-testing-id)').get().split('-')[0]
            category_urls = top_category_sel.css('.navbar-subcategory__item a')

            for category_url in category_urls:
                url = category_url.css('a::attr(href)').get()
                category_tree = top_menu_id + '%2F' + top_menu_id + '_' + url.split('/')[-2].replace('-', '_').replace(
                    'and_', '').replace('womens', 'WW').replace('mens', 'MW')
                page_url = url.replace(':', '%3A').replace('/', '%2F')
                final_url = 'https://fsm6.attraqt.com/zones-js.aspx?version=19.3.8&siteId=eddfa3c1-7e81-4cea-84a4-' \
                            '0f5b3460218a&UID=acb428d3-f3e9-d884-d2cf-42b16c58110f&referrer=&sitereferrer=&pageurl=' + \
                            page_url + '&zone0=banner&zone1=category&zone2=advert1&zone3=advert2&zone4=advert3&' \
                                       'facetmode=html&mergehash=false&culture=en-GB&currency=GBP&language=en-GB&' \
                                       'config_categorytree=' + category_tree
                yield response.follow(final_url, callback=self.parse_category)

    def parse_category(self, response):
        whiteStuff_parser = WhiteStuffParser()
        js_response = response.body_as_unicode()
        html_response = Selector(text=json.loads(re.findall('LM.buildZone\((.+)\);', js_response)[1])['html'])
        next_page = html_response.css('[rel="next"]::attr(href)').get()

        if next_page:
            url = next_page.replace(':', '%3A').replace('/', '%2F').replace('#', '%23').replace('=', '%3d')
            next_url = 'https://fsm6.attraqt.com/zones-js.aspx?version=19.3.8&siteId=eddfa3c1-7e81-4cea-84a4-' \
                       '0f5b3460218a&UID=acb428d3-f3e9-d884-d2cf-42b16c58110f&referrer=&sitereferrer=&pageurl=' + url \
                       + response.url[response.url.find('&zone0'):].replace('html', 'data').replace('true', 'false')
            yield response.follow(next_url, callback=self.parse_category)

        products_urls = html_response.css('.product-tile__title ::attr(href)').getall()
        for product_url in products_urls:
            final_url = 'https://www.whitestuff.com' + product_url
            yield response.follow(final_url, callback=whiteStuff_parser.parse_details)


class WhiteStuffItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    img_urls = scrapy.Field()
    skus = scrapy.Field()

