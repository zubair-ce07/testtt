import urllib.parse
from enum import Enum

from scrapy import Request
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import CrawlSpider, Rule
from w3lib.url import add_or_replace_parameter


class SizeType(Enum):
    First = 1
    Second = 2
    Third = 3


class SheegoSpider(CrawlSpider):
    name = 'sheego'
    allowed_domains = ['www.sheego.de']
    start_urls = ['https://www.sheego.de/']
    variant_url = 'https://www.sheego.de/index.php?'

    rules = (Rule(LinkExtractor(restrict_css=(['.mainnav--top', '.js-next']))),
             Rule(LinkExtractor(restrict_css=('.product__top')), callback="parse_product_detail"),)

    def parse_product_detail(self, response):
        item = {}
        item['meta'] = {}
        item['retailor_sku'] = self.retailor_sku(response)
        item['name'] = self.product_name(response)
        item['brand'] = self.brand(response)
        item['description'] = self.description(response)
        item['url'] = self.url(response)
        item['care'] = self.care(response)
        item['privious_price'], item['price'], item['currency'] = self.product_pricing(response)
        item['categories'] = self.categories(response)
        item['image_urls'] = []
        item['skus'] = {}
        item['meta']['requests'] = self.colour_requests(item, response)
        yield self.next_request(item)

    def parse_colour(self, response):
        item = response.meta['item']
        item['image_urls'] += self.images_url(response)
        item['meta']['requests'] = self.size_requests(response)
        yield self.next_request(item)

    def parse_size(self, response):
        item = response.meta['item']
        item['meta']['requests'] = self.size2_request(response)
        yield self.next_request(item)

    def parse_skus(self, response):
        item = response.meta['item']
        item['skus'].update(self.sku(response))
        yield self.next_request(item)

    def next_request(self, item):
        if item['meta']['requests']:
            request = item['meta']['requests'].pop(0)
            request.meta['item'] = item
            return request
        del item['meta']
        return item

    def int_price(self, price):
        return int(price.replace('.', '')) if price else ''

    def privious_price(self, response):
        privious_price = response.css('.product__price__wrong::text').re('(\d+,?\d*)') or ''
        if privious_price:
            privious_price = privious_price[0].replace(',', '.')
        return privious_price

    def colour_url(self, query_parameters):
        query_string = urllib.parse.urlencode(query_parameters)
        colour_url = self.variant_url + query_string
        return colour_url

    def size2_verselids(self, response):
        xpath = '//*[contains(@class,"size")]/select[not(contains(@class,"at-size"))]/option/@value'
        return response.xpath(xpath).extract()

    def size2(self, response):
        return response.css('.at-dv-size2::text').extract_first()

    def param_cl(self, response):
        return response.css('script.js-ads-script').re("window.ads.cl\s?=\s?'(.*)';window.ads.anid")[0]

    def retailor_sku(self, response):
        return response.css('.js-artNr::text').extract()[0].strip()[:6]

    def description(self, response):
        return response.css('meta[name="description"]::attr(content)').extract_first()

    def url(self, response):
        return response.css('meta[property="og:url"]::attr(content)').extract_first()

    def sizes_varselid(self, response):
        return response.css('.at-size-box ::attr(data-varselid)').extract()

    def length_type_varselids(self, response):
        return response.css('.at-size-type-box ::attr(value)').extract()

    def length_type(self, response):
        return response.css('.at-dv-size-type::text').extract_first()

    def colours_varselid(self, response):
        return response.css('.color ::attr(data-varselid)').extract()

    def colour(self, response):
        return response.css('.at-dv-color::text').extract_first()

    def size(self, response):
        return response.css('.at-size-box option[selected="selected"]::text').extract_first().strip()

    def is_instock(self, response):
        css = 'meta[itemprop="availability"]::attr(content)'
        availability = response.css(css).extract_first() or ''
        return 'InStock' in availability

    def images_url(self, response):
        return response.css('.p-details__image__thumb__container a::attr(href)').extract()

    def brand(self, response):
        return response.css('meta[itemprop="manufacturer"]::attr(content)').extract_first()

    def product_name(self, response):
        return response.css('h1[itemprop="name"]::text').extract_first().strip()

    def care(self, response):
        return [" ".join(item.split()) for item in response.css('div.p-details__careSymbols template ::text').extract()]

    def categories(self, response):
        return response.css('.breadcrumb__item ::text').extract()

    def product_pricing(self, response):
        price = response.css('meta[itemprop="price"]::attr(content)').extract_first()
        currency = response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()
        privious_price = self.privious_price(response)
        price = self.int_price(price)
        privious_price = self.int_price(privious_price)
        return privious_price, price, currency

    def colour_requests(self, item, response):
        requests = []
        param_cl = self.param_cl(response)
        colours_varselids = self.colours_varselid(response)
        for colour_varselid in colours_varselids:
            query_parameters = {
                'anid': item['retailor_sku'],
                'cl': param_cl,
                'varselid[0]': colour_varselid,
            }
            colour_url = self.colour_url(query_parameters)
            request = Request(url=colour_url, callback=self.parse_colour)
            requests.append(request)
        return requests

    def size_requests(self, response):
        length_type_varselids = self.length_type_varselids(response)
        size_varselids = self.sizes_varselid(response)
        size2_varselids = self.size2_verselids(response)
        sizes_type = SizeType.First
        if length_type_varselids:
            size_varselids = length_type_varselids
            sizes_type = SizeType.Third
        elif size2_varselids:
            sizes_type = SizeType.Second
        requests = response.meta['item']['meta']['requests']
        for size_varselid in size_varselids:
            size_url = add_or_replace_parameter(response.url, 'varselid[1]', size_varselid)
            request = Request(url=size_url,
                              meta={
                                  'sizes_type': sizes_type
                              })

            if sizes_type is SizeType.First:
                request.callback = self.parse_skus
            else:
                request.callback = self.parse_size
            requests.append(request)
        return requests

    def size2_request(self, response):
        requests = response.meta['item']['meta']['requests']
        sizes_type = response.meta['sizes_type']
        size2_varselids = []
        if sizes_type is SizeType.Second:
            size2_varselids = self.size2_verselids(response)
        elif sizes_type is SizeType.Third:
            size2_varselids = self.sizes_varselid(response)
        for size2_varselid in size2_varselids:
            size_url = add_or_replace_parameter(response.url, 'varselid[2]', size2_varselid)
            request = Request(url=size_url,
                              callback=self.parse_skus,
                              meta={
                                  'sizes_type': response.meta['sizes_type']
                              })
            requests.append(request)
        return requests

    def sku(self, response):
        privious_price, price, currency = self.product_pricing(response)
        colour = self.colour(response)
        size = self.size(response)
        stock = self.is_instock(response)
        sizes_type = response.meta['sizes_type']
        if sizes_type is SizeType.Second:
            size2 = self.size2(response)
            size = f'{size}_{size2}'
        elif sizes_type is SizeType.Third:
            length_type = self.length_type(response)
            size = f'{size}_{length_type}'
        sku_key = f'{colour}_{size}'.replace(' ', '_')
        sku_value = {
            'price': price,
            'currency': currency,
            'size': size,
            'colour': colour,
            'privious_price': privious_price
        }
        if not stock:
            sku_value['Out of Stock'] = True
        sku = {
            sku_key: sku_value
        }
        return sku

