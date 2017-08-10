import re
from urllib.parse import urlencode

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from sheego.items import Product


# utilit methods
def clean_list(data):
    temp = []
    for item in data:
        temp.append(item.strip())
    return temp


def create_color_urls(color_ids, product_id):
    color_urls = []
    base_url = 'https://www.sheego.de/index.php?'
    for color_id in color_ids:
        params = urlencode({'anid': product_id, 'cl': 'oxwarticledetails', 'varselid[0]': color_id,
                            'ajaxdetails': 'adsColorChange'})
        color_urls.append(base_url + params)
    return color_urls


def create_size_list(response, size_list, out_of_stock=False):
    sku = {}
    for size in size_list:
        size_info = {'size': size, 'color': response.css('span.js-color-value::text').extract_first().lstrip('– '),
                     'current_price': re.search(r'\d.+', response.css(
                         'span.at-lastprice::text').extract_first().strip()).group(), }
        if response.css('span.at-wrongprice'):
            size_info.update({'regular_price': re.search(r'\d.+', response.css(
                'span.at-wrongprice::text').extract_first().strip()).group()})
        if out_of_stock:
            size_info.update({'out_of_stock': True})
        sku.update({'{}_{}'.format(response.css('span.js-color-value::text').extract_first().lstrip('– '),
                                   size): size_info})
    return sku


class SheegoSpider(CrawlSpider):
    name = 'sheego'
    allowed_domains = ['www.sheego.de']
    start_urls = ['https://www.sheego.de/damenmode/',
                  'https://www.sheego.de/waesche-und-bademode/',
                  'https://www.sheego.de/damenschuhe/']
    rules = (
        Rule(LinkExtractor(
            restrict_css="a.js-next")),
        Rule(LinkExtractor(
            restrict_css='a.product__top'), callback="parse_product"),)

    def parse_product(self, response):
        product = Product()
        self.url(response, product)
        product_id = self.retailer_id(response, product)
        self.product_name(response, product)
        self.brand(response, product)
        self.details(response, product)
        product['image_urls'] = []
        product['skus'] = []
        color_urls = create_color_urls(response.css('span.colorspots__item::attr(data-varselid)').extract(), product_id)
        yield scrapy.Request(color_urls.pop(), callback=self.parse_sku,
                             meta={'product': product, 'color_urls': color_urls})

    def parse_sku(self, response):
        color_urls = response.meta.get('color_urls')
        product = response.meta.get('product')
        product['image_urls'] += response.css('a#magic::attr(href)').extract()
        sku = {}
        sku.update(create_size_list(response, clean_list(response.css('div.at-dv-size-button::text').extract())))
        sku.update(
            create_size_list(response, clean_list(response.css('div.sizespots__item--disabled::text').extract()), True))
        product['skus'].append(sku)
        if color_urls:
            yield scrapy.Request(color_urls.pop(), callback=self.parse_sku,
                                 meta={'product': product, 'color_urls': color_urls})
        else:
            yield product

    # functions for scraping fields
    @staticmethod
    def url(response, product):
        product['url'] = response.url.split('?')[0]

    @staticmethod
    def retailer_id(response, product):
        product_id = re.search(r'(\d+)', response.css('.js-artNr::text').extract_first()).group()
        product['retailer_id'] = product_id
        return product_id

    @staticmethod
    def product_name(response, product):
        product['name'] = response.css('h1[itemprop=name]::text').extract_first().strip()

    @staticmethod
    def brand(response, product):
        if response.css('.p-details__brand a'):
            product['brand'] = response.css('.p-details__brand a::text').extract_first().strip()
        else:
            product['brand'] = response.css('.p-details__brand::text').extract_first().strip()

    @staticmethod
    def details(response, product):
        product_details = {'bulletpoints': response.css('div.at-dv-article-details ul li::text').extract()}
        if response.css('[itemprop=description] p'):
            description = response.css('[itemprop=description] p::text').extract_first()
        else:
            description = clean_list(response.css('[itemprop=description]::text').extract())
        product_details.update({'description': description})
        details_key = response.css('div.at-dv-article-details b::text').extract()
        details_value = response.css('div.at-dv-article-details p::text').extract()[1:]
        product_details.update(dict(zip(details_key, details_value)))
        # features and materials
        if len(response.css('table.p-details__material')) > 1:
            feature_rows = response.css('table.p-details__material')[0].css('tr')
            feature_descriptions = clean_list(feature_rows.css('span::text').extract())
            feature_values = list(filter(None, clean_list(feature_rows.css('td::text').extract())))
            product_details.update({'features': dict(zip(feature_descriptions, feature_values))})
            material_rows = response.css('table.p-details__material')[1].css('tr')
        else:
            material_rows = response.css('table.p-details__material')[0].css('tr')
        material_descriptions = clean_list(material_rows.css('span::text').extract())
        material_values = list(filter(None, clean_list(material_rows.css('td::text').extract())))
        product_details.update({'materials': dict(zip(material_descriptions, material_values))})
        product['details'] = product_details
