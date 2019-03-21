import json
import re
from urllib.parse import urljoin

from scrapy.spiders import CrawlSpider, Request
from w3lib.url import add_or_replace_parameter

from ck_crawler.items import CkCrawlerItem


class ckCrawler(CrawlSpider):

    name = 'ck-fr-crawl'
    allowed_domains = ['calvinklein.fr']
    start_urls = ['https://www.calvinklein.fr/homme', 'https://www.calvinklein.fr/femme']

    products_url = 'https://www.calvinklein.fr/'
    image_url_t = 'https://calvinklein-eu.scene7.com/is/image/CalvinKleinEU/{}_{}?$main$'

    def parse_start_url(self, response):
        category_r = re.compile('= ({.*});', re.DOTALL)
        css = 'script:contains(\'window.app["mainNavigation"]\') ::text'
        raw_category = json.loads(response.css(css).re_first(category_r))

        for category in raw_category['navigation'][0]:
            for sub_category in category['subMenu']:
                for url in sub_category['subMenu']:
                    yield Request(url=urljoin(self.products_url, url['url']),
                                  callback=self.parse_pagination)

    def parse_pagination(self, response):
        products_r = re.compile('= ({.*});', re.DOTALL)
        css = 'script:contains(\'window.app["productList"]\') ::text'
        raw_products = json.loads(response.css(css).re_first(products_r))

        yield from [Request(url=urljoin(self.products_url, rel_url), callback=self.parse_product)
                    for rel_url in [i['relatedCombis'][0]['pdp'] for i in raw_products['catalogEntryNavView']]]

        if 'scrollPage' not in response.url and raw_products['noOfPages'] > 1:
            yield from [Request(url=add_or_replace_parameter(response.url, 'scrollPage', page),
                                callback=self.parse_pagination) for page in range(2, raw_products['noOfPages'])]

    def parse_product(self, response):
        item = CkCrawlerItem()
        raw_sku = self.raw_sku(response)
        raw_product = self.raw_product(response)

        item['lang'] = 'fr'
        item['url'] = self.product_url(response)
        item['name'] = self.product_name(raw_product)
        item['market'] = self.product_market(raw_sku)
        item['skus'] = self.skus(raw_sku, raw_product)
        item['brand'] = self.product_brand(raw_product)
        item['gender'] = self.product_gender(raw_product)
        item['image_urls'] = self.image_urls(raw_product)
        item['category'] = self.product_category(raw_product)
        item['description'] = self.product_description(raw_product)
        item['retailer_sku'] = self.product_retailer_sku(raw_product)

        return item

    def product_url(self, response):
        return response.url

    def product_market(self, raw_sku):
        return raw_sku['countryCode']

    def product_name(self, raw_product):
        return raw_product['name']

    def product_brand(self, raw_product):
        return raw_product['brandName']

    def product_gender(self, raw_product):
        return raw_product['sizeGuideGender']

    def product_retailer_sku(self, raw_product):
        return raw_product['productId']

    def product_pricing(self, raw_sku, raw_product):
        pricing = {'currency': raw_sku['currencyCode']}
        pricing['price'] = raw_product['price']['price']
        return pricing

    def product_category(self, raw_product):
        return raw_product['primaryCategory'].split('|')[-1]

    def raw_sku(self, response):
        sku_r = re.compile('= (.*?);', re.DOTALL)
        css = 'script:contains(\'window.app["app"]\') ::text'
        return json.loads(response.css(css).re_first(sku_r))

    def raw_product(self, response):
        product_r = re.compile('= ({.*})', re.DOTALL)
        css = 'script:contains(\'window.app["product"]\') ::text'
        return json.loads(response.css(css).re_first(product_r))

    def product_description(self, raw_product):
        return self.clean(raw_product['details']['description'])

    def clean(self, raw_text):
        if type(raw_text) is list:
            return [re.sub('(\r)*(\t)*(\n)*(BR)*[<>/]', ' ', i) for i in raw_text]
        return re.sub('(\r)*(\t)*(\n)*(BR)*[<>/]', ' ', raw_text)

    def image_urls(self, raw_product):
        image_urls = []
        raw_images = raw_product['details']['combis']['data']

        for colour_id in [i['colourCode'] for i in raw_images]:
            for image in range(1, [i['imageCount'] for i in raw_images][0]):
                image_urls.append(self.image_url_t.format(colour_id, 'alternate'+str(image)))
            image_urls.append(self.image_url_t.format(colour_id, 'main'))

        return image_urls

    def skus(self, raw_sku, raw_product):
        skus = {}
        sku_id = self.product_retailer_sku(raw_product)
        common_sku = self.product_pricing(raw_sku, raw_product)
        raw_product = raw_product['details']['attributes']

        for colour in raw_product['PRODUCT_ATTR_PRODUCT_ATTR_COLOUR']['values'].values():
            for size in raw_product['PRODUCT_ATTR_SIZE_FR']['values'].values():
                sku = common_sku.copy()
                sku['colour'] = colour['label']

                if not size['selectableStock']:
                    sku['out_of_stock'] = True

                sku['size'] = size['label']
                skus[f'{sku_id}_{colour["label"]}_{size["label"]}'] = sku

        return skus
