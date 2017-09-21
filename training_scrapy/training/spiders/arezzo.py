from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
import datetime
import re
from training.utils import pricing


class ArezzoSpider(CrawlSpider):
    name = 'arrezo-br'
    gender = 'women'
    language = 'pt'

    care = 'Material'
    visited_products = set()

    listing_css = ['.arz-nav']
    product_css = ['.arz-product-wrapper .arz-cover-link']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, ), callback='parse_listing'),
        Rule(LinkExtractor(restrict_css=product_css, ), callback='parse_product'),
    )

    start_urls = [
        'https://www.arezzo.com.br',
    ]

    def parse_listing(self, response):
        yield from self.parse(response)

        url = self.next_page_url(response)
        if url:
            yield Request(url=url, callback=self.parse_listing)

    def parse_product(self, response):
        retailer_sku = self.product_retailer_sku(response)
        if retailer_sku in self.visited_products:
            return
        self.visited_products.add(retailer_sku)

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
        size_unavailable_css = '.arz-disabled'
        skus = []
        color = self.product_color(response)
        for size_s in response.css(size_css):
            out_of_stock = False
            if size_s.css(size_unavailable_css):
                out_of_stock = True
            size = size_s.css('span::text').extract_first().strip()
            sku = self.pricing(response)
            sku.update(
                {
                    'sku_id': '{color}_{size}'.format(color=color, size=size),
                    'size': size,
                    'color': color,
                }
            )

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
        return 'Disney x Arezzo' if 'Disney x Arezzo' in self.product_raw_name(response) else 'Arezzo'

    def merch_info(self, response):
        name = self.product_raw_name(response)
        return ['PRE-SALE'] if '[PRE VENDA]' in name else []

    def product_image_urls(self, response):
        images_url_css = '.arz-product-gallery-thumb img::attr(data-original)'
        return response.css(images_url_css).extract()

    def product_description(self, response):
        description_css = '.arz-description p:nth-child(2)::text'
        return response.css(description_css).extract()

    def pricing(self, response):
        css = '.arz-product-price .arz-new-price::text,.arz-product-price .arz-old-price::text,.arz-product-price::text'
        regex = '\d+[\.\d+]*\,?\d*|$'
        return pricing(prices=response.css(css).extract(), regex=regex, comma=',', point='.')

    def product_color(self, response):
        characteristics = self.product_characteristics(response)
        for characteristic in characteristics:
            if 'Cor:' in characteristic:
                return characteristic.replace('Cor:', '').strip()

    def product_care(self, response):
        characteristics = self.product_characteristics(response)
        return [characteristic.strip() for characteristic in characteristics if self.care in characteristic]

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
