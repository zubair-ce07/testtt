# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider
from base import clean
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst
import json
from scrapy.http import Request
from scrapy.utils.url import url_query_parameter, add_or_replace_parameter


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

        garment['gender'] = self.product_gender(garment['name'].lower(), garment['gender'])
        garment['merch_info'] = self.merch_info(hxs)
        garment['image_urls'] = self.image_urls(hxs)
        garment['skus'] = self.skus(hxs)
        return garment

    def skus(self, hxs):
        skus = {}
        skus_data = self.take_first(clean(hxs.select("//div[@data-module-type='SkuSelector']//@data-product-variants")))
        skus_data = json.loads(skus_data)['variants']

        previous_price, price, currency = self.product_pricing(hxs)

        for sku_data in skus_data:
            size = sku_data['sizeTitle']
            sku = {
                'price': price,
                'currency': 'CAD',
                'size': self.one_size if size in ['N/S', 'NS'] else size,
                'colour': sku_data['colorTitle'],
                'out_of_stock': sku_data['available'] == 0,
            }

            if sku_data['colorTitle'] == '99 NO COLOR':
                sku.pop('colour')
            if previous_price:
                sku['previous_prices'] = [previous_price]

            skus[sku_data['code']] = sku

        return skus

    def product_id(self, hxs):
        return self.take_first(clean(hxs.select("//em[contains(@class,'description-item-num')]//text()")
                                     .re("Item #:(.*)")))

    def product_brand(self, hxs):
        return (self.take_first(clean(hxs.select("//div[contains(@class,'description-blurb-logo')]//a/@href")
                .re('brands\/(.*).html'))) or '').title().replace('-', ' ')

    def image_urls(self, hxs):
        images_data = self.take_first(clean(hxs.select("//div[contains(@class,'preview-gallery')]//@data-product")))
        images_data = json.loads(images_data)['imageDetails'].values()
        return ['https:' + y['imagePath'] for x in images_data for y in x]

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//h1[@class='global-page-header__title']//text()"))).lower()\
            .replace(self.product_brand(hxs).lower(), '').title()

    def product_category(self, hxs):
        return clean([x.strip('/') for x in clean(hxs.select("//div[@class='page-breadcrumb']//text()"))])[1:]

    def product_gender(self, name, default_gender):
        for x, y in self.gender_map:
            if x in name:
                return y
        return default_gender

    def product_description(self, hxs):
        return clean(hxs.select("//*[contains(text(),'           Features')]/following-sibling::div//text() |"
                                " //div[contains(@class,'description-blurb-text')]//p[1]//text()"))

    def product_care(self, hxs):
        return clean(hxs.select("//*[contains(text(), 'Specifications')]/following-sibling::div//text()"))

    def merch_info(self, hxs):
        if hxs.select("//div[@class='product-detail__options']//div[@class='product-detail__promotion']"):
            return ["Web Exclusive"]


class SportChekCrawlSpider(BaseCrawlSpider, Mixin):
    #: We do not want to crawl "Electronics" under "Deals & Offers"
    #: https://www.sportchek.ca/categories/equipment.html
    #: We do not want to crawl "Equipment"
    #: https://www.sportchek.ca/categories/chek-tech.html

    name = Mixin.retailer + '-crawl'
    parse_spider = SportChekParseSpider()

    def parse_start_url(self, response):
        product_url_t = 'https://' + self.allowed_domains[0] + '%s.html'

        json_data = json.loads(response.body)
        total_products = int(json_data['resultCount']['total'])
        products_data = json_data['products']

        for product in products_data:
            yield Request(url=product_url_t % product['pagePath'], callback=self.parse_item,
                          meta={'trail': self.add_trail(response), 'gender': response.meta['gender']})

        page_no = int(url_query_parameter(response.url, 'page'))
        if total_products - (page_no * 50) > 0:
            next_page_url = add_or_replace_parameter(response.url, 'page', str(page_no + 1))
            yield Request(next_page_url, callback=self.parse_start_url, meta={'trail': self.add_trail(response),
                                                                              'gender': response.meta['gender']})

    def add_trail(self, response):
        trail_part = [(response.meta.get('link_text', ''), response.url)]
        return response.meta.get('trail', []) + trail_part