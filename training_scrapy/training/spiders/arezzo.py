from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
import datetime
import re
from training.utils import clean_and_convert_price, currency_information


class ArezzoSpider(CrawlSpider):
    name = 'arrezo-br'
    gender = 'women'
    language = 'pt'

    visited_references = dict()

    rules = (
        Rule(LinkExtractor(restrict_css=['.arz-nav'], ), callback='request_next_page'),
        Rule(LinkExtractor(restrict_css=['.arz-product-wrapper .arz-cover-link'], ), callback='parse_product'),
    )

    start_urls = [
        'https://www.arezzo.com.br',
    ]

    def request_next_page(self, response):
        yield from self.parse(response)

        url = self.next_page_url(response)
        if url:
            yield Request(url=url, callback=self.request_next_page)

    def parse_product(self, response):
        retailer_sku = self.product_retailer_sku(response)
        if retailer_sku in self.visited_references:
            return

        self.visited_references[retailer_sku] = True
        product = {
            'crawl_start_time': datetime.datetime.now(),
            'name': self.product_name(response),
            'brand': self.product_brand(response),
            'merch_info': self.merch_info(response),
            'retailer_sku': retailer_sku,
            'category': self.product_category(response),
            'image_urls': self.product_image_urls(response),
            'description': self.product_description(response),
            'sku': self.product_skus(response),
            'care': self.product_care(response),
            'gender': self.gender,
            'spider_name': self.name,
            'lang': self.language,
            'url': response.url,
            'url_original': response.url
        }

        if self.product_out_of_stock(response):
            product['out_of_stock'] = True

        return product

    def product_skus(self, response):
        size_css = '.arz-btn-secondary.arz-sm'
        size_unavailable_css = '.arz-disabled span::text'
        size_available_css = ':not(.arz-disabled) span::text'
        skus = []
        price, currency = self.product_price_and_currency(response)
        color = self.product_color(response)
        for selector in response.css(size_css):
            out_of_stock = False
            if selector.css(size_unavailable_css):
                out_of_stock = True
                size = selector.css(size_unavailable_css).extract_first().strip()
            else:
                size = selector.css(size_available_css).extract_first().strip()
            sku = {
                'sku_id': '{color}_{size}'.format(color=color, size=size),
                'size': size,
                'currency': currency,
                'price': price,
                'color': color,
            }

            if out_of_stock:
                sku['out_of_stock'] = out_of_stock

            skus.append(sku)

        return skus

    def product_name(self, response):
        remove_string_regex = '(\s*Disney x Arezzo\s*|\s*\[PRE VENDA\]\s*-\s*|\|)+'
        name = self.product_raw_name(response)
        return re.sub(remove_string_regex,'',name).strip()

    def product_category(self, response):
        category_css = '#breadcrumb a::text'
        categories = response.css(category_css).extract()
        return categories[1:-1] if categories else []

    def product_brand(self, response):
        brands = ['Disney x Arezzo', 'Arezzo']
        name = self.product_raw_name(response)
        return brands[0] if brands[0] in name else brands[1]

    def merch_info(self, response):
        name = self.product_raw_name(response)
        return ['PRE-SALE'] if '[PRE VENDA]' in name else []

    def product_information(self, key, raw_information):
        for information in raw_information:
            if key in information:
                return information.replace(key, '').strip()
        return None

    def product_image_urls(self, response):
        images_url_css = '.arz-product-gallery-thumb img::attr(data-original)'
        return response.css(images_url_css).extract()

    def product_description(self, response):
        description_css = '.arz-description p:nth-child(2)::text'
        return response.css(description_css).extract()

    def product_price_and_currency(self, response):
        price_css = ['.arz-product-detail .arz-product-price .arz-new-price::text',
                     '.arz-product-detail .arz-product-price::text']
        for css in price_css:
            price = response.css(css).extract_first()
            if price:
                currency = currency_information(price)
                return (clean_and_convert_price(price, currency[1]), currency[0])
        return (None, None)

    def product_color(self, response):
        characteristics = self.product_characteristics(response)
        for characteristic in characteristics:
            if 'Cor:' in characteristic:
                return characteristic.replace('Cor:', '').strip()
        return None

    def product_care(self, response):
        care = 'Material'
        characteristics = self.product_characteristics(response)
        return [characteristic.strip() for characteristic in characteristics if care in characteristic]

    def product_retailer_sku(self, response):
        return response.url.split('/')[-1]

    def product_raw_name(self, response):
        title_css = '.arz-product-detail .arz-product-title span::text'
        return response.css(title_css).extract_first()

    def product_characteristics(self, response):
        information_css = '.arz-product-description-fix :not([class])::text'
        return [value.strip() for value  in response.css(information_css).extract() if value.strip()]

    def product_out_of_stock(self, response):
        out_of_stock_css = '.arz-product-available-info .arz-product-line span::text'
        return False if response.css(out_of_stock_css).extract_first() == 'Comprar' else True

    def page_category(self, response):
        category_css = '#breadcrumb a::text'
        categories = response.css(category_css).extract()
        return categories[1:] if categories else None

    def next_page_url(self, response):
        url = 'https://www.arezzo.com.br/c/{category}?q=%3Arelevance%3A&sort=creation-time&page={number}&text='
        next_page_css = '.arz-pagination .active span::text'

        next_page = response.css(next_page_css).extract_first()

        categories = self.page_category(response)
        page_category = '/'.join(categories)

        if next_page and page_category:
            return url.format(category=page_category.lower(), number=next_page)
