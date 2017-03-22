import re
import codecs
from itertools import product

from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, TextResponse

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
    html_tag_removal_regex = '<.*?>'
    description_tab_index = 0
    care_tab_index = 1

    def parse(self, response):
        links = LinkExtractor(
            restrict_css=('#nav',), deny=('sale',)).extract_links(response)
        for link in links:
            yield next(self.parse_category_url(link.url))

    def parse_category_url(self, category_url):
        pre_known_product_values = {}
        if 'herren' in category_url:
            pre_known_product_values['gender'] = 'mens'
        elif 'girls' in category_url:
            pre_known_product_values['gender'] = 'girls'
        elif 'boys' in category_url:
            pre_known_product_values['gender'] = 'boys'
        elif 'looks' not in category_url:
            pre_known_product_values['gender'] = 'womens'

        category_tree = category_url.split('.com/')[1]
        url = self.category_pagination_url_t.format(category_url, category_tree)
        meta = {
            'pre_known_product_values': pre_known_product_values
        }
        yield Request(url, callback=self.parse_category, meta=meta)

    def parse_category(self, response):
        text_response = self.response_containing_products(response)
        yield next(self.parse_category_products(text_response))

        if not response.meta.get('follow_pagination_urls', True):
            return

        next_page_urls = text_response.css('#pagnTop .pagnnum a::attr(href)').extract()
        for url in next_page_urls:
            page_url = self.base_url + url
            category_tree = url.split('?')[0].lstrip('/')
            complete_url = self.category_pagination_url_t.format(
                page_url, category_tree
            )
            meta = {
                'follow_pagination_urls': False,
                'pre_known_product_values': text_response.meta['pre_known_product_values']
            }
            yield Request(complete_url, callback=self.parse_category, meta=meta)

    def response_containing_products(self, response):
        escaped_html = re.search('"html":"(.*)",', response.text).group(1)
        unescaped_html = codecs.escape_decode(escaped_html.encode())[0].decode()
        dummy_request = Request(self.base_url, meta=response.meta)
        return TextResponse(url='', body=unescaped_html.encode(), request=dummy_request)

    def parse_category_products(self, response):
        products_html = response.css('.prod')
        for item in products_html:
            meta = self.parse_product_html(item)
            meta['pre_known_product_values'] = response.meta['pre_known_product_values']
            complete_url = self.base_url + meta['product_url']
            yield Request(complete_url, callback=self.parse_product, meta=meta)

    def parse_product_html(self, selector):
        price, currency = selector.css('#price::text').extract_first().split(' ')
        try:
            previous_price = selector.css('#atrwas::text').extract_first().split(' ')[0]
        except AttributeError:
            previous_price = ''

        return {
            'price': price,
            'previous_price': previous_price,
            'currency': currency,
            'product_url': selector.css('.prod-name a::attr(href)').extract_first(),
            'product_id': selector.css('::attr(data-id)').extract_first(),
            'name': selector.css('::attr(data-name)').extract_first()
        }

    def parse_product(self, response):
        boohoo_product = GenericProduct()
        boohoo_product['brand'] = ''
        boohoo_product['market'] = ''
        boohoo_product['merch_info'] = []
        boohoo_product['category'] = []
        boohoo_product['url'] = response.url
        boohoo_product['product_id'] = response.meta['product_id']
        boohoo_product['name'] = response.meta['name']
        boohoo_product['image_urls'] = self.parse_image_urls(response)
        boohoo_product['skus'] = self.parse_skus(response)
        boohoo_product.update(response.meta['pre_known_product_values'])

        tab_selector = response.css('#collateral-accordion')
        boohoo_product['care'] =\
            self.parse_description_tab(tab_selector, self.care_tab_index)
        boohoo_product['description'] =\
            self.parse_description_tab(tab_selector, self.description_tab_index)

        return boohoo_product

    def parse_description_tab(self, selector, tab_index):
        try:
            text = selector.css('dd')[tab_index].extract()
        except (AttributeError, IndexError):
            return []
        else:
            return [re.sub(self.html_tag_removal_regex, '', text)]

    def parse_image_urls(self, response):
        image_urls = response.css('.product-image-thumbs .thumbnail img::attr(src)').extract()
        return [url.split('?')[0] for url in image_urls]

    def parse_skus(self, response):
        sizes = response.css(
            '#configurable_swatch_international_size a::attr(title)').extract()
        colors = response.css('#configurable_swatch_color a::attr(name)').extract()

        skus = {}
        for size, colour in product(sizes, colors):
            skus['{}_{}'.format(colour, size)] = {
                'size': size,
                'colour': colour,
                'price': response.meta['price'],
                'previous_price': response.meta['previous_price'],
                'currency': response.meta['currency']
            }
        return skus
