from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
import datetime
import re


class ArezzoSpider(CrawlSpider):
    name = 'arrezo-br'
    gender = 'women'
    language = 'pt'
    currency = 'BRL'

    brand_regex = '(\s*Disney x Arezzo\s*\|\s*)'
    merch_info_regex = '(\s*\[PRE VENDA\]\s*\-?\s*)'

    rules = (
        Rule(LinkExtractor(restrict_css=['.arz-nav'], ), callback='request_next_page'),
    )

    start_urls = [
        'https://www.arezzo.com.br',
    ]

    def request_next_page(self, response):
        links = self.multiple_products(response)
        if links:
            url = self.next_page_url(response)
            if url:
                links.append(Request(url=url, callback=self.request_next_page))
            return links

    def multiple_products(self, response):
        links = []
        product_links = self.product_links(response)
        for link in product_links:
            links.append(Request(url=link.url, callback=self.parse_product))
        return links

    def product_links(self, response):
        product_link_css = '.arz-product-wrapper .arz-cover-link'
        link_extractor = LinkExtractor(restrict_css=[product_link_css], )
        return link_extractor.extract_links(response)

    def parse_product(self, response):
        product = {}
        product['crawl_start_time'] = datetime.datetime.now()

        raw_product_name = self.product_raw_name(response)
        raw_information = self.product_raw_information(response)
        size_list = self.product_size(response)
        price = self.product_price(response)

        color = self.product_color(raw_information)

        product['name'] = self.product_name(raw_product_name)
        product['brand'] = self.product_brand(raw_product_name)
        product['merch_info'] = self.merch_info(raw_product_name)
        product['retailer_sku'] = self.product_retailer_sku(raw_information)
        product['category'] = self.product_category(response)
        product['image_urls'] = self.product_image_urls(response)
        product['description'] = self.product_description(response)
        product['sku'] = self.product_skus(color, size_list, price)
        product['out_of_stock'] = self.product_out_of_stock(product['sku'])
        product['gender'] = self.gender
        product['spider_name'] = self.name
        product['lang'] = self.language
        product['url'] = response.url
        product['url_original'] = response.url

        return product

    def product_skus(self, color, size_list, price):
        sku_list = []
        for size, available in size_list:
            sku = {}
            sku['out_of_stock'] = not available
            sku['sku_id'] = '{color}_{size}'.format(color=color, size=size)
            sku['size'] = size
            sku['currency'] = self.currency
            sku['price'] = price
            sku_list.append(sku)
        return sku_list

    def product_name(self, values):
        name = ' '.join(values)
        name = re.sub(self.merch_info_regex, '', name)
        return re.sub(self.brand_regex, '', name)

    def product_category(self, response):
        category_css = '#breadcrumb a::text'
        categories = response.css(category_css).extract()
        if categories:
            categories.pop(0)
            categories.pop()
        return categories

    def product_brand(self, name):
        name = ' '.join(name)
        brand = re.search(self.brand_regex, name)
        if brand:
            return 'Disney x Arezzo'
        return 'Arezzo'

    def product_information(self, regex, raw_information_list):
        for raw_information in raw_information_list:
            status = re.search(regex, raw_information)
            if status:
                return re.sub(regex, '', raw_information)
        return None

    def product_size(self, response):
        size_available_css = '.arz-btn-secondary.arz-sm:not(.arz-disabled) span::text'
        size_not_available_css = '.arz-btn-secondary.arz-sm.arz-disabled span::text'

        available_size = response.css(size_available_css).extract()
        not_available_size = response.css(size_not_available_css).extract()
        return [(size, True) for size in available_size] + [(size, False) for size in not_available_size]

    def merch_info(self, name):
        name = ' '.join(name)
        status = re.search(self.merch_info_regex, name)
        if status:
            return ['PRE-SALE']
        return []

    def product_image_urls(self, response):
        images_url_css = '.arz-product-gallery-thumb img::attr(data-original)'
        return response.css(images_url_css).extract()

    def product_description(self, response):
        description_css = '.arz-description p:nth-child(2)::text'
        return response.css(description_css).extract()

    def product_price(self, response):
        price_regex = '\s*R\s*\$\s*'
        price_css = '.arz-product-detail .arz-product-price::text'
        raw_price = response.css(price_css).extract()
        return self.product_information(price_regex, raw_price)

    def product_color(self, raw_information):
        color_regex = '\A\s*Cor\s*:\s*'
        return self.product_information(color_regex, raw_information)

    def product_retailer_sku(self, raw_information):
        retailer_sku_regex = '\A\s*Referência\s*:\s*'
        return self.product_information(retailer_sku_regex, raw_information)

    def product_raw_name(self, response):
        title_css = '.arz-product-detail .arz-product-title span::text'
        return response.css(title_css).extract()

    def product_raw_information(self, response):
        information_css = '.arz-product-description-fix ::text'
        return response.css(information_css).extract()

    def product_out_of_stock(self, skus):
        for sku in skus:
            if not sku.get('out_of_stock', False):
                return False
        return True

    def page_category(self, response):
        category_css = '#breadcrumb a::text'
        categories = response.css(category_css).extract()
        if categories:
            categories.pop(0)
        return categories

    def next_page_url(self, response):
        url = 'https://www.arezzo.com.br/c/{category}?q=%3Arelevance%3A&sort=creation-time&page={number}&text='
        next_page_css = '.arz-pagination .active span::text'

        next_page = response.css(next_page_css).extract_first()

        categories = self.page_category(response)
        page_category = '/'.join(categories)

        if next_page and page_category:
            return url.format(category=page_category.lower(), number=next_page)
        return None
