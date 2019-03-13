import json
import re
from urllib.parse import urljoin

from scrapy.spiders import CrawlSpider, Request
from w3lib.url import add_or_replace_parameter

from ck_crawler.items import CkCrawlerItem


class CkCrawler(CrawlSpider):

    name = 'ck-fr-crawl'
    allowed_domains = ['calvinklein.fr']
    start_urls = ['https://www.calvinklein.fr/homme', 'https://www.calvinklein.fr/femme']

    url_t = 'https://www.calvinklein.fr/'
    img_url_t = 'https://calvinklein-eu.scene7.com/is/image/CalvinKleinEU/{}_{}?$main$'

    def parse_start_url(self, response):
        css = """script:contains('window.app["mainNavigation"]') ::text"""
        regex = re.compile('= ({.*});', re.DOTALL)
        raw_product = json.loads(response.css(css).re_first(regex))

        for category in raw_product['navigation'][0]:
            for sub_category in category['subMenu']:
                for url in sub_category['subMenu']:
                    yield Request(url=urljoin(self.url_t, url['url']), callback=self.parse_pagination)

    def parse_pagination(self, response):
        css = """script:contains('window.app["productList"]') ::text"""
        regex = re.compile('= ({.*});', re.DOTALL)
        raw_product = json.loads(response.css(css).re_first(regex))
        pages = raw_product['noOfPages']

        for rel_url in [i['relatedCombis'][0]['pdp'] for i in raw_product['catalogEntryNavView']]:
            yield Request(url=urljoin(self.url_t, rel_url), callback=self.parse_product)

        if 'scrollPage' not in response.url and pages > 1:
            for page in range(2, pages):
                next_url = add_or_replace_parameter(response.url, 'scrollPage', page)
                yield Request(url=next_url, callback=self.parse_pagination)

    def parse_product(self, response):
        item = CkCrawlerItem()
        raw_product = self.raw_product(response)

        item['lang'] = 'fr'
        item['url'] = self.product_url(response)
        item['name'] = self.product_name(raw_product)
        item['market'] = self.product_market(response)
        item['brand'] = self.product_brand(raw_product)
        item['skus'] = self.skus(response, raw_product)
        item['gender'] = self.product_gender(raw_product)
        item['image_urls'] = self.image_urls(raw_product)
        item['category'] = self.product_category(raw_product)
        item['description'] = self.product_description(raw_product)
        item['retailer_sku'] = self.product_retailer_sku(raw_product)

        return item

    def product_url(self, response):
        return response.url

    def product_name(self, raw_product):
        return raw_product['name']

    def product_brand(self, raw_product):
        return raw_product['brandName']

    def product_market(self, response):
        raw_sku = self.raw_sku(response)
        return raw_sku['countryCode']

    def product_gender(self, raw_product):
        return raw_product['sizeGuideGender']

    def product_retailer_sku(self, raw_product):
        return raw_product['productId']

    def product_pricing(self, response, raw_product):
        raw_sku = self.raw_sku(response)
        pricing = {'currency': raw_sku['currencyCode']}
        pricing['price'] = raw_product['price']['price']
        return pricing

    def product_category(self, raw_product):
        return raw_product['primaryCategory'].split('|')[-1]

    def raw_sku(self, response):
        css = """script:contains('window.app["app"]') ::text"""
        regex = re.compile('= (.*?);', re.DOTALL)
        return json.loads(response.css(css).re_first(regex))

    def raw_product(self, response):
        css = """script:contains('window.app["product"]') ::text"""
        regex = re.compile('= ({.*})', re.DOTALL)
        return json.loads(response.css(css).re_first(regex))

    def product_description(self, raw_product):
        return raw_product['details']['description'].replace('<br>', '')

    def image_urls(self, raw_product):
        img_urls = []
        raw_imgs = raw_product['details']['combis']['data']
        colour_ids = [i['colourCode'] for i in raw_imgs]
        img_count = [i['imageCount'] for i in raw_imgs]

        for colour_id in colour_ids:
            for img_id in range(1, img_count[0]):
                img_urls.append(self.img_url_t.format(colour_id, 'alternate'+str(img_id)))
            img_urls.append(self.img_url_t.format(colour_id, 'main'))

        return img_urls

    def skus(self, response, raw_product):
        skus = {}
        sku_id = self.product_retailer_sku(raw_product)
        common_sku = self.product_pricing(response, raw_product)

        for colour in raw_product['details']['attributes']['PRODUCT_ATTR_PRODUCT_ATTR_COLOUR']['values'].values():
            for size in raw_product['details']['attributes']['PRODUCT_ATTR_SIZE_FR']['values'].values():
                sku = common_sku.copy()
                sku['colour'] = colour['label']

                if not size['selectableStock']:
                    sku['out_of_stock'] = True

                sku['size'] = size['label']
                skus[f'{sku_id}_{colour["label"]}_{size["label"]}'] = sku

        return skus
