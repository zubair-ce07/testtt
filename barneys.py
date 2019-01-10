import json

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

        item['retailer_sku'] = retailer_sku
        item['name'] = self.extract_name(response)
        item['gender'] = self.extract_gender(response)
        item['spider_name'] = 'barneys'
        item['brand'] = self.extract_brand(response)
        item['url'] = response.url
        item['trail'] = response.meta.get('trail', [])
        item['category'] = self.extract_categories(response)
        item['retailer'] = self.extract_retailer()
        item['market'] = self.extract_market()
        item['description'] = self.extract_description(response)
        item['care'] = self.extract_care(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['skus'] = self.extract_skus(response)

        return item

    def is_new_item(self, product):
        if product and product not in self.seen_ids:
            self.seen_ids.add(product)
            return True

        return False

    def extract_product_id(self, response):
        xpath = "//script[contains(., 'digitalData')]/text()"
        return response.xpath(xpath).re_first('productID.*?"(.*?)"')

    def extract_description(self, response):
        description = response.css('.pdpReadMore .visible-xs.visible-sm *::text').extract()
        return [des.strip() for des in description if des.strip()] if description else []

    def extract_name(self, response):
        xpath = "//script[contains(., 'digitalData')]/text()"
        return response.xpath(xpath).re_first('productName.*?"(.*?)"')

    def extract_care(self, response):
        return response.css('div[class="visible-xs visible-sm"] ul li::text').extract()

    def extract_brand(self, response):
        xpath = "//script[contains(., 'digitalData')]/text()"
        return response.xpath(xpath).re_first('brand.*?"(.*?)"')

    def extract_categories(self, response):
        xpath = "//script[contains(., 'digitalData')]/text()"
        category = response.xpath(xpath).re('subCategory2.*?"(.*?)"')
        return [cat.strip() for cat in category if cat.strip()]

    def extract_image_urls(self, response):
        image_urls = response.css('.product-image-carousel .primary-image::attr(src)').extract()
        image_urls += response.css('.product-single-image .primary-image::attr(src)').extract()
        return image_urls

    def extract_skus(self, response):
        skus = {}
        common_sku = extract_price_details(self.extract_price(response))
        common_sku['colour'] = self.extract_colour(response)

        sizes = self.extract_all_sizes(response)
        available_sizes = self.extract_available_sizes(response)

        for size in sizes:
            sku = common_sku.copy()
            sku['size'] = size
            if size not in available_sizes:
                sku['out_of_stock'] = True

            skus[f"{sku['colour']}_{sku['size']}"] = sku

        return skus

    def extract_colour(self, response):
        xpath = "//script[contains(., 'digitalData')]/text()"
        return response.xpath(xpath).re_first('color.*?"(.*?)"')

    def extract_market(self):
        return 'Sweden'

    def extract_gender(self, response):
        gender_info = response.xpath('//span[@id="fp-data"]/@data-gender').extract()
        gender_info += self.extract_categories(response)
        return extract_gender(''.join(gender_info))

    def extract_price(self, response):
        css = '.atg_store_productPrice:not([class^="promotion-callout-msg"])::text'
        price_details = [price.strip() for price in response.css(css).extract() if price.strip() and '%' not in price]
        price_details += self.extract_currency()
        return price_details

    def extract_retailer(self):
        return 'barneys'

    def extract_currency(self):
        return 'SEK'

    def extract_all_sizes(self, response):
        sizes = response.css('[id="fp_allSizes"]::attr(value)').extract_first()
        return json.loads(sizes) if sizes else ['One Size']

    def extract_available_sizes(self, response):
        available_sizes = response.css('[id="fp_availableSizes"]::attr(value)').extract_first()
        return json.loads(available_sizes) if available_sizes else ['One Size']


class BarneysSpider(CrawlSpider):
    name = 'barneys-crawl-spider'
    allowed_domains = ['www.barneys.com']
    start_urls = ['https://www.barneys.com/']
    product_parser = ProductParser()

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 '
                      'Safari/537.36'
    }

    product_css = ['[id="ajaxGlobalNav"]', '.topnav-level-1']
    listing_css = ['[id="main-container"]']
    rules = [
        Rule(LinkExtractor(restrict_css=product_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_item')
    ]

    def start_requests(self):
        self.start_urls.append('https://www.barneys.com/global/ajaxGlobalNav.jsp')
        return [Request(url, callback=self.parse) for url in self.start_urls]

    def parse(self, response):
        trail = response.meta.get('trail', [])
        title = self.extract_title(response)
        if title:
            trail = trail + [[title, response.url]]

        for request in super().parse(response):
            request.meta['trail'] = trail
            request.cookies['usr_currency'] = 'SE-SEK'
            yield request

    def parse_item(self, response):
        return self.product_parser.parse(response)

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        if title:
            title = title.split('|')[0].strip()

        return title
