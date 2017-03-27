import re
import codecs
from itertools import product

from scrapy import Selector
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from crawler_tasks.items import GenericProduct


class BoohooSpider(Spider):
    name = 'boohoo'
    allowed_domains = ['de.boohoo.com', 'fsm2.attraqt.com']
    start_urls = ['http://de.boohoo.com/']
    base_url = 'http://de.boohoo.com'
    category_pagination_url_t = \
        'http://fsm2.attraqt.com/zones-js.aspx?siteId=df08ca30-5d22-4ab2-978a-cf3dbbd6a9a5' \
        '&zone0=prod_list_prods&currency=EUR' \
        '&pageurl={}' \
        '&config_categorytree={}'

    description_tab_name = 'Beschreibung'
    care_tab_name = 'Produktdetails & Pflege'
    gender_mapping = {
        'herren': 'mens',
        'girls': 'girls',
        'boys': 'boys'
    }

    def parse(self, response):
        links = LinkExtractor(
            restrict_css=('#nav',), deny=('sale',)).extract_links(response)
        for link in links:
            yield self.parse_category_url(link.url)

    def parse_category_url(self, category_url):
        pre_known_product_values = {}
        for gender in self.gender_mapping:
            if gender in category_url:
                pre_known_product_values['gender'] = self.gender_mapping[gender]
                break
        else:
            if 'looks' not in category_url:
                pre_known_product_values['gender'] = 'womens'

        return self.make_category_request(category_url, pre_known_product_values)

    def make_category_request(self, category_url, pre_known_product_values):
        category_tree = category_url.split('.com/')[1]
        url = self.category_pagination_url_t.format(category_url, category_tree)
        meta = {
            'pre_known_product_values': pre_known_product_values
        }
        return Request(url, callback=self.parse_category, meta=meta)

    def parse_category(self, response):
        html_selector = self.response_html_selector(response)
        for product_request in self.parse_category_products(
                html_selector, response.meta):
            yield product_request

        if not response.meta.get('follow_pagination_urls', True):
            return

        next_page_urls = html_selector.css('#pagnTop .pagnnum ::attr(href)').extract()
        for url in next_page_urls:
            page_url = self.base_url + url
            category_tree = url.split('?')[0].lstrip('/')
            complete_url = self.category_pagination_url_t.format(
                page_url, category_tree
            )
            meta = response.meta.copy()
            meta['follow_pagination_urls'] = False
            yield Request(complete_url, callback=self.parse_category, meta=meta)

    def response_html_selector(self, response):
        escaped_html = re.search('"html":"(.*)",', response.text).group(1)
        unescaped_html = codecs.escape_decode(escaped_html.encode())[0]
        return Selector(text=unescaped_html, type='html')

    def parse_category_products(self, html_selector, meta):
        product_requests = []
        products_html = html_selector.css('.prod')
        for item in products_html:
            product_url = item.css('.prod-name ::attr(href)').extract_first()
            complete_url = self.base_url + product_url
            product_requests.append(
                Request(complete_url, callback=self.parse_product, meta=meta))
        return product_requests

    def parse_product(self, response):
        boohoo_product = GenericProduct()
        boohoo_product['brand'] = ''
        boohoo_product['market'] = ''
        boohoo_product['merch_info'] = []
        boohoo_product['category'] = []
        boohoo_product['url'] = response.url
        boohoo_product['product_id'] = response.css('#prodSKU::text').extract_first()
        boohoo_product['name'] = response.css('#pageName::text').extract_first()
        boohoo_product['image_urls'] = self.parse_image_urls(response)
        boohoo_product['skus'] = self.parse_skus(response)
        boohoo_product.update(response.meta['pre_known_product_values'])

        tab_selector = response.css('#collateral-accordion')
        if tab_selector:
            boohoo_product['care'] =\
                self.parse_description_tab(tab_selector, self.care_tab_name)
            boohoo_product['description'] =\
                self.parse_description_tab(tab_selector, self.description_tab_name)
        else:
            boohoo_product['care'] = []
            boohoo_product['description'] = []

        return boohoo_product

    def parse_description_tab(self, selector, tab_name):
        tab_names = selector.css('dt').css('::text').extract()
        if tab_name in tab_names:
            index = tab_names.index(tab_name)
            return selector.css('dd')[index].css('::text').extract()
        return []

    def parse_image_urls(self, response):
        image_urls = response.css('.product-image-thumbs .thumbnail ::attr(src)').extract()
        return [url.split('?')[0] for url in image_urls]

    def parse_skus(self, response):
        special_price = response.css('.special-price .price::text')
        if special_price:
            price, currency = special_price[0].re('\S+')
            prev_price = response.css('.old-price .price::text')[0].re('\S+')[0]
        else:
            price, currency = response.css('.regular-price .price::text')[0].re('\S+')
            prev_price = ''

        sizes = response.css(
            '#configurable_swatch_international_size a::attr(title)').extract()
        colors = response.css('#configurable_swatch_color a::attr(name)').extract()

        skus = {}
        for size, colour in product(sizes, colors):
            skus['{}_{}'.format(colour, size)] = {
                'size': size,
                'colour': colour,
                'price': price,
                'previous_price': prev_price,
                'currency': currency
            }
        return skus
