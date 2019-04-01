import re
import json
from urllib.parse import urljoin

from scrapy.link import Link
from w3lib.url import add_or_replace_parameter
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule

from ck_crawler.items import CalvinkleinCrawlerItem


class ProductLinkExtractor(LinkExtractor):

    def extract_links(self, response):

        if not response.meta.get('raw_products'):
            return []

        return [Link(urljoin(response.url, url)) for url in [i['relatedCombis'][0]['pdp']
                for i in response.meta.get('raw_products')['catalogEntryNavView']]]


class CalvinkleinCrawler(CrawlSpider):

    name = 'calvinklein-fr-crawl'
    allowed_domains = ['calvinklein.fr']
    start_urls = ['https://www.calvinklein.fr/homme', 'https://www.calvinklein.fr/femme']
    image_url_t = 'https://calvinklein-eu.scene7.com/is/image/CalvinKleinEU/{}_{}?$main$'

    rules = (
        Rule(ProductLinkExtractor(), callback='parse_product'),
    )

    def parse_start_url(self, response):
        category_r = re.compile('= ({.*});', re.DOTALL)
        css = 'script:contains(\'window.app["mainNavigation"]\') ::text'
        raw_category = json.loads(response.css(css).re_first(category_r))

        return [response.follow(url['url'], callback=self.parse_pagination) for category in
                raw_category['navigation'][0] for sub_category in category['subMenu'] for url in
                sub_category['subMenu']]

    def parse_pagination(self, response):
        products_r = re.compile('= ({.*});', re.DOTALL)
        css = 'script:contains(\'window.app["productList"]\') ::text'
        raw_products = json.loads(response.css(css).re_first(products_r))

        return [Request(url=add_or_replace_parameter(response.url, 'scrollPage', page),
                meta={'raw_products': raw_products}, callback=self.parse) for
                page in range(1, raw_products['noOfPages'])]

    def parse_product(self, response):
        item = CalvinkleinCrawlerItem()
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
            return [re.sub('(\r)*(\t)*(\n)*', '', i) for i in raw_text]
        return re.sub('(\r)*(\t)*(\n)*', '', raw_text)

    def skus(self, raw_sku, raw_product):
        skus = {}
        common_sku = self.product_pricing(raw_sku, raw_product)
        raw_product = raw_product['details']['attributes']

        for colour in raw_product['PRODUCT_ATTR_PRODUCT_ATTR_COLOUR']['values'].values():
            for size in raw_product['PRODUCT_ATTR_SIZE_FR']['values'].values():
                sku = common_sku.copy()
                sku['colour'] = colour['label']

                if not size['selectableStock']:
                    sku['out_of_stock'] = True

                sku['size'] = size['label']
                skus[f'{colour["label"]}_{size["label"]}'] = sku

        return skus

    def image_urls(self, raw_product):
        raw_images = raw_product['details']['combis']['data']
        return [self.image_url_t.format(colour_id, f'alternate{image_id}') for colour_id in [i['colourCode']
                for i in raw_images] for image_id in range(1, [i['imageCount'] for i in raw_images][0])]
