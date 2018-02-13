import urllib.parse

import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import CrawlSpider, Rule


class SheegoSpider(CrawlSpider):
    name = 'sheego'
    allowed_domains = ['www.sheego.de']
    start_urls = ['https://www.sheego.de/']
    variant_url = 'https://www.sheego.de/index.php?'

    rules = (Rule(LinkExtractor(restrict_css=(['.mainnav--top', 'a.js-next']))),
             Rule(LinkExtractor(restrict_css=('.product__top')), callback="parse_product_detail"),)

    def parse_product_detail(self, response):
        item = {}
        item['retailor_sku'] = self.retailor_sku(response)
        item['name'] = self.name(response)
        item['brand'] = self.brand(response)
        item['description'] = self.description(response)
        item['url'] = self.url(response)
        item['care'] = self.care(response)
        item['price'] = self.price(response)
        item['currency'] = self.currency(response)
        param_cl = self.param_cl(response)
        item['image_urls'] = []
        item['skus'] = {}
        colours_varselids = self.colours_varselid(response)
        requests = self.colour_requests(item, param_cl, colours_varselids)
        self.request(requests)

    def colour_requests(self, item, param_cl, colours_varselids):
        requests = []
        for colour_varselid in colours_varselids:
            query_parameters = {
                'anid': item['retailer_sku'],
                'cl': param_cl,
                'varselid[0]': colour_varselid,
            }
            colour_url = self.make_url(query_parameters)
            request = scrapy.Request(url=colour_url, callback=self.parse_colour)
            request.meta['item'] = item
            requests.append(request)

    def parse_colour(self, response):
        item = response.meta['item']
        requests = response.meta['requests']
        item['image_urls'] += self.images_url(response)
        size_type_varselids = self.size_type_varselids(response)
        if not size_type_varselids:
            size_varselids = self.sizes_varselid(response)
            size2_varselids = self.size2_verselids(response)
            sizes_type = 2
        else:
            size_varselids = size_type_varselids
            size2_varselids = self.sizes_varselid(response)
            sizes_type = 3
        requests = self.size_requests(requests, size_varselids, sizes_type)
        self.request(requests)

    def size_requests(self, requests, size_varselids, sizes_type):
        for size_varselid in size_varselids:
            query_parameters = {'varselid[1]': size_varselid}
            query_string = urllib.parse.urlencode(query_parameters)
            size_url = response.url + '&' + query_string
            if size2_varselids:
                request = scrapy.Request(url=size_url,
                                         callback=self.parse_size,
                                         meta={
                                             'sizes_type': sizes_type
                                         })
            else:
                request = scrapy.Request(url=size_url,
                                         callback=self.parse_skus,
                                         meta={
                                             'sizes_type': 1
                                         })
            request.meta['item'] = item
            requests.append(request)
        return  requests

    def parse_size(self, response):
        item = response.meta['item']
        requests = response.meta['requests']
        sizes_type = response.meta['sizes_type']
        if sizes_type is 2:
            size2_varselids = self.size2_verselids(response)
        elif sizes_type is 3:
            size2_varselids = self.sizes_varselid(response)
        for size2_varselid in size2_varselids:
            query_parameters = {'varselid[2]': size2_varselid}
            query_string = urllib.parse.urlencode(query_parameters)
            size_url = response.url + '&' + query_string
            request = scrapy.Request(url=size_url,
                                     callback=self.parse_skus,
                                     meta={
                                         'sizes_type': response.meta['sizes_type']
                                     })
            request.meta['item'] = item
            requests.append(request)
        self.request(requests)

    def parse_skus(self, response):
        item = response.meta['item']
        sizes_type = response.meta['sizes_type']
        price = self.price(response)
        currency = self.currency(response)
        colour = self.colour(response)
        stock = self.is_instock(response)
        size = self.size(response)
        if sizes_type is 2:
            size2 = self.size2(response)
            size = '{0}_{1}'.format(size, size2)
        elif sizes_type is 3:
            size2 = self.size_type(response)
            size = '{0}_{1}'.format(size, size2)
        sku = self.generate_sku(price, currency, size, colour, stock)
        item['skus'].update(sku)
        requests = response.meta['requests']
        if requests:
            request = requests.pop(0)
            request.meta['item'] = item
            request.meta['requests'] = requests
            yield request
        else:
            yield item

    def size2_verselids(self, response):
        selectors = response.css('.size')
        if len(selectors) is 2:
            return selectors[0].css('option:attr(value)').extract()
        return None

    def generate_sku(self, price, currency, size, colour, stock):
        sku_key = (colour + '_' + size).replace(' ', '_')
        sku_value = {
            'price': price,
            'currency': currency,
            'size': size,
            'colour': colour,
            'in_stock': stock
        }
        sku = {
            sku_key: sku_value
        }
        return sku

    def request(self, requests):
        if requests:
            request = requests.pop(0)
            request.meta['requests'] = requests
            yield request

    def colour_url(self, query_parameters):
        query_string = urllib.parse.urlencode(query_parameters)
        colour_url = self.variant_url + query_string
        return colour_url

    def size2(self, response):
        return response.css('.at-dv-size2::text').extract_first()

    def param_cl(self, response):
        return response.css('script.js-ads-script').re("window.ads.cl\s?=\s?'(.*)';window.ads.anid")[0]

    def retailor_sku(self, response):
        return response.css('.js-artNr::text').extract()[0].strip()[:6]

    def description(self, response):
        return response.css('meta[name="description"]::attr(content)').extract_first()

    def title(self, response):
        return response.css('meta[property="og:title"]::attr(content)').extract_first()

    def url(self, response):
        return response.css('meta[property="og:url"]::attr(content)').extract_first()

    def price(self, response):
        return response.css('meta[itemprop="price"]::attr(content)').extract_first()

    def sizes_varselid(self, response):
        return response.css('.at-size-box ::attr(data-varselid)').extract()

    def size_type_varselids(self, response):
        return response.css('.at-size-type-box ::attr(value)').extract()

    def size_type(self, response):
        return response.css('.at-dv-size-type::text').extract_first()

    def colours_varselid(self, response):
        return response.css('.color ::attr(data-varselid)').extract()

    def colour(self, response):
        return response.css('.at-dv-color::text').extract_first()

    def currency(self, response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

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

    def name(self, response):
        return response.css('h1[itemprop="name"]::text').extract_first().strip()

    def care(self, response):
        return response.css('div.p-details__careSymbols template ::text').extract()

