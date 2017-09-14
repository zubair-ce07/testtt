import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
import datetime
import re

class ArezzoSpider(CrawlSpider):
    name = 'arrezo-br'
    gender = 'women'
    language = 'pt'
    currency = 'BRL'

    price_regex = '\s*R\s*\$\s*'
    brand_regex = '(\s*Disney x Arezzo\s*\|\s*)'
    color_regex = '\A\s*Cor\s*:\s*'
    merch_info_regex = '(\s*\[PRE VENDA\]\s*\-?\s*)'
    retailer_sku_regex = '\A\s*Referência\s*:\s*'

    title_css = '.arz-product-detail .arz-product-title span::text'
    price_css = '.arz-product-detail .arz-product-price::text'
    category_css = '#breadcrumb a::text'
    images_url_css = '.arz-product-gallery-thumb img::attr(data-original)'
    description_css = '.arz-description p:nth-child(2)::text'
    size_available_css = '.arz-btn-secondary.arz-sm:not(.arz-disabled) span::text'
    size_not_available_css = '.arz-btn-secondary.arz-sm.arz-disabled span::text'
    information_css = '.arz-product-description-fix ::text'

    rules = (

        Rule(
            LxmlLinkExtractor(
                restrict_css=['.arz-navbar', '.pagination'],
            ),
        ),
        Rule(
            LxmlLinkExtractor(
                restrict_css=['.arz-home-sliders .arz-cover-link'],
            ),
            callback='parse_product',
        ),
    )

    start_urls = [
        'https://www.arezzo.com.br',
    ]

    def parse_product(self, response):
        product = {}
        product['crawl_start_time'] = datetime.datetime.now()

        raw_product_name = response.css(self.title_css).extract()

        product['name'] = self.get_product_name(raw_product_name)
        product['brand'] = self.get_product_brand(raw_product_name)
        product['merch_info'] = self.get_merch_info(raw_product_name)
        product['category'] = self.get_product_category(response.css(self.category_css).extract())
        product['image_urls'] = response.css(self.images_url_css).extract()
        product['description'] = response.css(self.description_css).extract()
        product['gender'] = self.gender
        product['spider_name'] = self.name
        product['lang'] = self.language
        product['url'] = response.url
        product['url_original'] = response.url

        raw_information = response.css(self.information_css).extract()

        product['retailer_sku'] = self.get_product_information(self.retailer_sku_regex, raw_information)

        color = self.get_product_information(self.color_regex, raw_information)
        size_list = self.get_product_size_list(response)
        raw_price = response.css(self.price_css).extract()
        price = self.get_product_information(self.price_regex, raw_price)

        product['sku'] = self.get_product_sku_list(color, size_list, price)
        product['out_of_stock'] = False if product['sku'] else True

        return product

    def get_product_sku_list(self, color, size_list, price):
        sku_list = []
        for size, available in size_list:
            sku = {}
            sku['out_of_stock'] = not available
            sku['gender'] = self.gender
            sku['sku_id'] = '{color}_{size}'.format(color=color, size=size)
            sku['size'] = size
            sku['currency'] = self.currency
            sku['price'] = price
            sku_list.append(sku)
        return sku_list

    def get_product_name(self, values):
        name = ' '.join(values)
        name = re.sub(self.merch_info_regex, '', name)
        return re.sub(self.brand_regex, '', name)

    def get_product_category(self, categories):
        if categories:
            categories.pop(0)
            categories.pop()
        return categories

    def get_product_brand(self, name):
        name = ' '.join(name)
        brand = re.search(self.brand_regex, name)
        if brand:
            return 'Disney x Arezzo'
        return 'Arezzo'

    def get_product_information(self, regex, raw_information_list):
        for raw_information in raw_information_list:
            status = re.search(regex, raw_information)
            if status:
                return re.sub(regex, '', raw_information)
        return None

    def get_product_size_list(self, response):
        available_size = response.css(self.size_available_css).extract()
        not_available_size = response.css(self.size_not_available_css).extract()
        return [(size, True) for size in available_size] + [(size, False) for size in not_available_size]

    def get_merch_info(self, name):
        name = ' '.join(name)
        status = re.search(self.merch_info_regex, name)
        if status:
            return ['PRE-SALE']
        return []