# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider
from base import clean
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst
import json
from scrapy.http import Request
from scrapy.utils.url import url_query_parameter, add_or_replace_parameter
import re


class Mixin(object):
    market = 'CA'
    retailer = 'sportchek-ca'
    allowed_domains = ['www.sportchek.ca', 'fgl.scene7.com']
    url_t = 'https://www.sportchek.ca/services/sportchek/search-and-promote/products?' \
            'x1=c.category-level-1&q1=%s&preselectedCategoriesNumber=1&page=1&count=50'

    start_urls_with_meta = [(url_t % 'Kids', {'gender': 'unisex-kids'}),
                            (url_t % 'Men', {'gender': 'men'}),
                            (url_t % 'Women', {'gender': 'women'}),
                            (url_t % 'Fan Shop', {'gender': 'men'}),
                            (url_t % 'Accessories', {'gender': 'unisex-adults'})]


class SportChekParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = "//div[contains(@class,'price-wrap ')]//span[contains(text(), '$')]//text()"
    take_first = TakeFirst()
    gender_map = (
        ('boy', 'boys'),
        ('girl', 'girls'),
        ('women', 'women'),
        ('men', 'men'),
        ('kid', 'unisex-kids'),
    )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        pid = self.product_id(hxs)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, hxs, response)

        garment['gender'] = self.product_gender(garment)
        garment['image_urls'] = self.image_urls(hxs)
        garment['skus'] = self.skus(hxs)
        garment['merch_info'] = self.merch_info(hxs)
        return garment

    def skus(self, hxs):
        skus = {}
        skus_xpath = "//div[@data-module-type='SkuSelector']//@data-product-variants"
        skus_data = self.take_first(clean(hxs.select(skus_xpath)))
        skus_data = json.loads(skus_data)['variants']

        try:
            previous_price, price, currency = self.product_pricing(hxs)
        except IndexError:
            previous_price = price = ''

        for sku_data in skus_data:
            size = sku_data['sizeTitle']
            sku = {
                'currency': self._CURRENCY_REMAP.get((self.market, currency), currency),
                'size': self.one_size if size in ['N/S', 'NS'] else size,
                'colour': sku_data['colorTitle'],
                'out_of_stock': sku_data['available'] == 0,
            }

            if sku_data['color'] == '99':
                sku.pop('colour')
            if price:
                sku['price'] = price
            if previous_price:
                sku['previous_prices'] = [previous_price]

            skus[sku_data['code']] = sku

        return skus

    def product_id(self, hxs):
        id_xpath = "//em[contains(@class,'description-item-num')]//text()"
        return self.take_first(clean(hxs.select(id_xpath).re("Item #:(.*)")))

    def product_brand(self, hxs):
        brand_xpath = "//div[contains(@class,'description-blurb-logo')]//a/@href"
        brand = self.take_first(clean(hxs.select(brand_xpath).re('brands\/(.*).html'))) or ''
        return brand.title().replace('-', ' ')

    def image_urls(self, hxs):
        images_xpath = "//div[contains(@class,'preview-gallery')]//@data-product"
        images_data = self.take_first(clean(hxs.select(images_xpath)))
        images_data = json.loads(images_data)['imageDetails'].values()

        return ['https:' + image['imagePath'] for color in images_data for image in color]

    def product_name(self, hxs):
        name = self.take_first(clean(hxs.select("//h1[@class='global-page-header__title']//text()")))
        return name.lower().replace(self.product_brand(hxs).lower(), '').title()

    def product_category(self, hxs):
        categories = clean(hxs.select("//div[@class='page-breadcrumb']//text()"))
        return clean([category.strip('/') for category in categories])[1:]

    def product_gender(self, garment):
        name_l = garment['name'].lower()
        for key_word, gender in self.gender_map:
            if key_word in name_l:
                return gender
        return garment['gender']

    def product_description(self, hxs):
        desc1_xpath = "//*[contains(text(),'Features')]/following-sibling::div//text()"
        desc2_xpath = "//div[contains(@class,'description-blurb-text')]//p[1]//text()"
        return clean(hxs.select(desc1_xpath + " | " + desc2_xpath))

    def product_care(self, hxs):
        care_xpath = "//*[contains(text(), 'Specifications')]/following-sibling::div//li[not(a)]//text()"
        return clean(hxs.select(care_xpath))

    def merch_info(self, hxs):
        merch_info_xpath = "//div[@class='product-detail__promo_desktop']//span//text()"
        merch_info = clean(hxs.select(merch_info_xpath))

        merch_info_str = ' '.join(merch_info)
        key_words = 'exclusive|online.only|price.shown.includes'
        if re.findall(key_words, merch_info_str, re.I):
            return merch_info


class SportChekCrawlSpider(BaseCrawlSpider, Mixin):
    #: We do not want to crawl "Electronics" under "Deals & Offers"
    #: https://www.sportchek.ca/categories/equipment.html
    #: We do not want to crawl "Equipment"
    #: https://www.sportchek.ca/categories/chek-tech.html

    name = Mixin.retailer + '-crawl'
    parse_spider = SportChekParseSpider()

    def parse_start_url(self, response):
        product_url_t = 'https://' + self.allowed_domains[0] + '%s.html'
        meta_data = {'trail': self.add_trail(response), 'gender': response.meta['gender']}

        json_data = json.loads(response.body)
        total_products = int(json_data['resultCount']['total'])
        products_data = json_data['products']

        for product in products_data:
            yield Request(url=product_url_t % product['pagePath'], callback=self.parse_item, meta=meta_data)

        page_no = int(url_query_parameter(response.url, 'page'))
        if total_products - (page_no * 50) > 0:
            next_page_url = add_or_replace_parameter(response.url, 'page', str(page_no + 1))
            yield Request(next_page_url, callback=self.parse_start_url, meta=meta_data)

    def add_trail(self, response):
        trail_part = [(response.meta.get('link_text', ''), response.url)]
        return response.meta.get('trail', []) + trail_part