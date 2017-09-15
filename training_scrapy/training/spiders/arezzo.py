from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
import datetime
from training.utils import clean_price, currency_name

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
        yield Request(url=url, callback=self.request_next_page) if url else None

    def parse_product(self, response):
        if self.visited(response):
            return

        product = {
            'crawl_start_time': datetime.datetime.now(),
            'name': self.product_name(response),
            'brand': self.product_brand(response),
            'merch_info': self.merch_info(response),
            'retailer_sku': self.product_retailer_sku(response),
            'category': self.product_category(response),
            'image_urls': self.product_image_urls(response),
            'description': self.product_description(response),
            'sku': self.product_skus(response),
            'gender': self.gender,
            'spider_name': self.name,
            'lang': self.language,
            'url': response.url,
            'url_original': response.url
        }
        product['out_of_stock'] = self.product_out_of_stock(product['sku'])

        return product

    def visited(self, response):
        if self.visited_references.get(self.product_retailer_sku(response), False):
            return True
        self.visited_references[self.product_retailer_sku(response)] = True
        return False

    def product_skus(self, response):
        product_size = self.product_size(response)
        price, currency = self.product_price_and_currency(response)
        color = self.product_color(response)

        skus = []
        for size, available in product_size.items():
            sku = {
                'out_of_stock': not available,
                'sku_id': '{color}_{size}'.format(color=color, size=size),
                'size': size,
                'currency': currency,
                'price': price,
                'color': color
            }
            skus.append(sku)

        return skus

    def product_name(self, response):
        remove_string = ['Disney x Arezzo', '[PRE VENDA]', '-']
        name = self.product_raw_name(response)
        for string in remove_string:
            if string in name:
                name = name.replace(string, '')
        return name.strip()

    def product_category(self, response):
        category_css = '#breadcrumb a::text'
        categories = response.css(category_css).extract()
        return categories[1:-1] if categories else None

    def product_brand(self, response):
        brands = ['Disney x Arezzo', 'Arezzo']
        name = self.product_raw_name(response)
        for brand in brands:
            if brand in name:
                return brand
        return 'Arezzo'

    def merch_info(self, response):
        tags = {
            '[PRE VENDA]': 'PRE-SALE'
        }
        merch_info_tags = list()
        name = self.product_raw_name(response)
        for key, value in tags.items():
            if key in name:
                merch_info_tags.append(value)
        return merch_info_tags

    def product_information(self, key, raw_information):
        for information in raw_information:
            if key in information:
                return information.replace(key, '').strip()
        return None

    def product_size(self, response):
        size_available_css = '.arz-btn-secondary.arz-sm:not(.arz-disabled) span::text'
        size_not_available_css = '.arz-btn-secondary.arz-sm.arz-disabled span::text'

        available_size = response.css(size_available_css).extract()
        not_available_size = response.css(size_not_available_css).extract()

        return {**{size: True for size in available_size}, **{size: False for size in not_available_size}}

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
                currency =  currency_name(price)
                return (clean_price(price), currency)
        return (None, None)

    def product_color(self, response):
        raw_information = self.product_raw_information(response)
        return self.product_information('Cor:', raw_information)

    def product_retailer_sku(self, response):
        return response.url.split('/')[-1]

    def product_raw_name(self, response):
        title_css = '.arz-product-detail .arz-product-title span::text'
        return response.css(title_css).extract_first()

    def product_raw_information(self, response):
        information_css = '.arz-product-description-fix :not([class])::text'
        return [value.strip() for value  in response.css(information_css).extract() if value.strip()]

    def product_out_of_stock(self, skus):
        for sku in skus:
            if not sku.get('out_of_stock', False):
                return False
        return True

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
        return None
