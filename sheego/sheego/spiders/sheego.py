import re
from urllib.parse import urlencode
from urllib import request

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.utils.response import open_in_browser

from sheego.items import Product


def clean_list(list):
    temp = []
    for item in list:
        temp.append(item.strip())
    return temp


def url(response, product):
    product['url'] = response.url.split('?')[0]


def brand(response, product):
    if response.css('.p-details__brand a'):
        product['brand'] = response.css('.p-details__brand a::text').extract_first().strip()
    else:
        product['brand'] = response.css('.p-details__brand::text').extract_first().strip()


def color(response, product):
    product['color'] = response.css('span.js-color-value::text').extract_first().lstrip('– ')


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
    product['details'] = product_details


def features(response, product):
    rows = response.css('table.p-details__material')[0].css('tr')
    desc = clean_list(rows.css('span::text').extract())
    values = list(filter(None, clean_list(rows.css('td::text').extract())))
    product['features'] = dict(zip(desc, values))


def material(response, product):
    if len(response.css('table.p-details__material')) > 1:
        rows = response.css('table.p-details__material')[1].css('tr')
    else:
        rows = response.css('table.p-details__material')[0].css('tr')
    desc = clean_list(rows.css('span::text').extract())
    values = list(filter(None, clean_list(rows.css('td::text').extract())))
    product['material'] = dict(zip(desc, values))


# def image_urls(response, product):
#     product['image_urls'] = response.css(
#         "div.product-image-gallery-thumbs.configurable *::attr(href)").extract()
#     # response.xpath("//div[@class='product-image-gallery-thumbs configurable']//@href").extract()

def name(response, product):
    product['name'] = response.css('h1[itemprop=name]::text').extract_first().strip()


def retailer_id(response, product):
    product['retailer_id'] = re.search(r'(\d+)', response.css('.js-artNr::text').extract_first()).group()


class SheegoSpider(CrawlSpider):
    name = 'sheego'
    allowed_domains = ['www.sheego.de']
    start_urls = ['https://www.sheego.de/damenschuhe/']
    rules = (
        # Rule(LinkExtractor(
        #     restrict_css="a.js-next")),
        Rule(LinkExtractor(
            restrict_css='a.product__top'), callback="parse_product"),)

    def parse_sku(self, response):
        urls = response.meta.get('urls')
        product = response.meta.get('product')
        sku = {'color': response.css('span.js-color-value::text').extract_first().lstrip('– '),
               'available_sizes': clean_list(response.css('div.at-dv-size-button::text').extract()),
               'out_of_stock_sizes': clean_list(response.css('div.sizespots__item--disabled::text').extract()),
               'current_price': response.css('span.at-lastprice::text').extract_first().strip(),
               }
        if response.css('span.at-wrongprice'):
            sku.update({'regular_price': response.css('span.at-wrongprice::text').extract_first().strip()})
        product['skus'].append(sku)
        if urls:
            c_url = urls.pop()
            yield scrapy.Request(c_url, callback=self.parse_sku, meta={'product': product, 'urls': urls})
        else:
            yield product

    def parse_product(self, response):
        product = Product()

        url(response, product)
        retailer_id(response, product)
        name(response, product)
        brand(response, product)
        details(response, product)
        features(response, product)
        material(response, product)
        # image_urls(response, product)
        product['skus'] = []
        product_id = re.search(r'(\d+)', response.css('.js-artNr::text').extract_first()).group()
        colors_list = response.css('span.colorspots__item::attr(data-varselid)').extract()
        base_url = 'https://www.sheego.de/index.php?'
        urls = []
        for color in colors_list:
            params = urlencode(
                {'anid': product_id, 'cl': 'oxwarticledetails', 'varselid[0]': color, 'ajaxdetails': 'adsColorChange'})
            curl = base_url + params
            urls.append(curl)
        c_url = urls.pop()
        yield scrapy.Request(c_url, callback=self.parse_sku, meta={'product': product, 'urls': urls})
