import json
import re

from scrapy import Spider, Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from item_structure import Item
from helpers import extract_price_details, extract_gender


class ProductParser(Spider):
    def __init__(self):
        self.seen_ids = set()

    def parse(self, response):
        item = Item()
        retailer_sku = self.extract_product_id(response)

        if not self.is_new_item(retailer_sku):
            return

        raw_product = self.extract_raw_product(response)
        item['retailer_sku'] = retailer_sku
        item['name'] = self.extract_name(raw_product)
        item['gender'] = self.extract_gender(raw_product, response)
        item['spider_name'] = 'barneys'
        item['brand'] = self.extract_brand(raw_product)
        item['url'] = response.url
        item['trail'] = response.meta.get('trail', [])
        item['category'] = self.extract_categories(raw_product)
        item['retailer'] = self.extract_retailer()
        item['market'] = self.extract_market()
        item['description'] = self.extract_description(response)
        item['care'] = self.extract_care(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['skus'] = self.extract_skus(raw_product, response)

        return item

    def is_new_item(self, product):
        if product and product not in self.seen_ids:
            self.seen_ids.add(product)
            return True

        return False

    def extract_product_id(self, response):
        return response.xpath("//script[contains(., 'digitalData')]/text()").re_first('productID.*?"(.*?)"')

    def extract_description(self, response):
        description = response.css('.pdpReadMore .visible-xs.visible-sm *::text').extract()
        return [des.strip() for des in description if des.strip()]

    def extract_name(self, raw_product):
        return raw_product['product']['StyleInfo']['productName']

    def extract_care(self, response):
        return response.css('div[class="visible-xs visible-sm"] ul li::text').extract()

    def extract_brand(self, raw_product):
        return raw_product['product']['StyleInfo']['brand']

    def extract_categories(self, raw_product):
        category = raw_product['page']['category']
        return [category['primaryCategory'], category['subCategory1'], category['subCategory2']]

    def extract_image_urls(self, response):
        css = '.product-image-carousel .primary-image::attr(src), .product-single-image .primary-image::attr(src)'
        return response.css(css).extract()

    def extract_skus(self, raw_product, response):
        skus = {}
        common_sku = extract_price_details(self.extract_price(response))
        common_sku['colour'] = self.extract_colour(raw_product)

        sizes = self.extract_all_sizes(response)
        available_sizes = self.extract_available_sizes(response)

        for size in sizes:
            sku = common_sku.copy()
            sku['size'] = size
            if size not in available_sizes:
                sku['out_of_stock'] = True

            skus[f"{sku['colour']}_{sku['size']}"] = sku

        return skus

    def extract_colour(self, raw_product):
        return raw_product['product']['SkuInfo'][0]['productInfo']['color']

    def extract_market(self):
        return 'Sweden'

    def extract_gender(self, raw_product, response):
        gender_info = response.xpath('//span[@id="fp-data"]/@data-gender').extract()
        gender_info += self.extract_categories(raw_product)
        return extract_gender(''.join(gender_info))

    def extract_price(self, response):
        css = '.atg_store_productPrice:not([class^="promotion-callout-msg"]) *::text'
        return [price.strip() for price in response.css(css).extract() if price.strip() and '%' not in price]

    def extract_retailer(self):
        return 'barneys'

    def extract_currency(self):
        return 'SEK'

    def extract_raw_product(self, response):
        xpath = "//script[contains(., 'digitalData')]/text()"
        raw_product = response.xpath(xpath).re_first('digitalData.*?({.*);')
        raw_product = re.sub("(\w+) : ", r'"\1" :', raw_product)
        return json.loads(raw_product)

    def extract_all_sizes(self, response):
        sizes = response.css('[id="fp_allSizes"]::attr(value)').extract_first()
        return json.loads(sizes) if sizes else ['One Size']

    def extract_available_sizes(self, response):
        available_sizes = response.css('[id="fp_availableSizes"]::attr(value)').extract_first()
        return json.loads(available_sizes) if available_sizes else ['One Size']


class BarneysSpider(CrawlSpider):
    name = 'barneys-crawl-spider'
    allowed_domains = ['www.barneys.com']
    start_urls = ['https://www.barneys.com/', 'https://www.barneys.com/global/ajaxGlobalNav.jsp']
    product_parser = ProductParser()

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 '
                      'Safari/537.36'
    }

    product_css = ['[id="ajaxGlobalNav"]', '.topnav-level-1']
    listing_css = ['[id="main-container"]']
    rules = [
        Rule(LinkExtractor(restrict_css=product_css), callback='parse', process_request='set_currency_cookie'),
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_item', process_request='set_currency_cookie')
    ]

    def parse(self, response):
        trail = response.meta.get('trail', [])
        title = self.extract_title(response)
        if title:
            trail = trail + [[title, response.url]]

        for request in super().parse(response):
            request.meta['trail'] = trail
            yield request

    def parse_item(self, response):
        return self.product_parser.parse(response)

    def set_currency_cookie(self, request):
        request.cookies['usr_currency'] = 'SE-SEK'
        return request

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        if title:
            title = title.split('|')[0].strip()

        return title
