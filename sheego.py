import urllib.parse

import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import CrawlSpider, Rule


class SheegoSpider(CrawlSpider):
    name = 'sheego'
    allowed_domains = ['www.sheego.de']
    start_urls = ['https://www.sheego.de/']
    base_url = 'https://www.sheego.de/index.php?'

    rules = (Rule(LinkExtractor(restrict_css=(['.mainnav--top', 'a.js-next']))),
             Rule(LinkExtractor(restrict_css=('a.product__top')), callback="parse_product_detail"),)

    def parse_product_detail(self, response):
        item = {}
        item['retailer_sku'] = self.get_retailor_sku(response)
        item['name'] = self.get_name(response)
        item['brand'] = self.get_brand(response)
        item['description'] = self.get_description(response)
        item['url'] = self.get_url(response)
        item['care'] = self.get_care(response)
        item['price'] = self.get_price(response)
        item['currency'] = self.get_currency(response)
        cl = self.get_param_cl(response)
        item['image_urls'] = []
        item['skus'] = {}
        requests = []
        colours_varselids = self.get_colours_varselid(response)
        for colour_varselid in colours_varselids:
            query_parameters = {
                'anid': item['retailer_sku'],
                'cl': cl,
                'varselid[0]': colour_varselid,
            }
            colour_url = self.make_url(query_parameters)
            request = scrapy.Request(url=colour_url, callback=self.parse_colour)
            request.meta['item'] = item
            requests.append(request)

        if requests:
            request = requests.pop(0)
            request.meta['requests'] = requests
            yield request

    def parse_colour(self, response):
        item = response.meta['item']
        requests = response.meta['requests']
        item['image_urls'] += self.get_images_url(response)
        length_varselids = self.get_length_varselids(response)
        if not length_varselids:
            size_varselids = self.get_sizes_varselid(response)
            size2_varselids = self.get_size2_verselids(response)
            sizes_type = 2
        else:
            size_varselids = length_varselids
            size2_varselids = self.get_sizes_varselid(response)
            sizes_type = 3
        for size_varselid in size_varselids:
            query_parameters = {'varselid[1]': size_varselid}
            query_string = urllib.parse.urlencode(query_parameters)
            size_url = response.url + '&' + query_string
            if size2_varselids:
                request = scrapy.Request(url=size_url,
                                         callback=self.parse_size,
                                         meta={
                                             'size2_varselids': size2_varselids,
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

        if requests:
            request = requests.pop(0)
            request.meta['requests'] = requests
            yield request

    def parse_size(self, response):
        item = response.meta['item']
        requests = response.meta['requests']
        size2_varselids = response.meta['size2_varselids']
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

        if requests:
            request = requests.pop(0)
            request.meta['requests'] = requests
            yield request

    def parse_skus(self, response):
        item = response.meta['item']
        sizes_type = response.meta['sizes_type']
        price = self.get_price(response)
        currency = self.get_currency(response)
        colour = self.get_colour(response)
        stock = self.get_is_instock(response)
        size = self.get_size(response)
        if sizes_type is 2:
            size2 = self.get_size2(response)
            size = '{0}_{1}'.format(size, size2)
        elif sizes_type is 3:
            size2 = self.get_length(response)
            size = '{0}_{1}'.format(size, size2)
        sku_key = (colour + '_' + size).replace(' ', '_')
        sku_data = {
            'price': price,
            'currency': currency,
            'size': size,
            'colour': colour,
            'in_stock': stock
        }
        current_sku = {
            sku_key: sku_data
        }
        item['skus'].update(current_sku)
        requests = response.meta['requests']
        if requests:
            request = requests.pop(0)
            request.meta['item'] = item
            request.meta['requests'] = requests
            yield request
        else:
            yield item

    def get_size2_verselids(self, response):
        selectors = response.css('.size')
        if len(selectors) is 2:
            return selectors[0].css('option:attr(value)').extract()
        return None

    def make_url(self, query_parameters):
        query_string = urllib.parse.urlencode(query_parameters)
        colour_url = self.base_url + query_string
        return colour_url

    def get_size2(self, response):
        return response.css('.at-dv-size2::text').extract_first()

    def get_param_cl(self, response):
        return response.css('script.js-ads-script').re("window.ads.cl\s?=\s?'(.*)';window.ads.anid")[0]

    def get_retailor_sku(self, response):
        return response.css('.js-artNr::text').extract()[0].strip()[:6]

    def get_description(self, response):
        return response.css('meta[name="description"]::attr(content)').extract_first()

    def get_title(self, response):
        return response.css('meta[property="og:title"]::attr(content)').extract_first()

    def get_url(self, response):
        return response.css('meta[property="og:url"]::attr(content)').extract_first()

    def get_price(self, response):
        return response.css('meta[itemprop="price"]::attr(content)').extract_first()

    def get_sizes_varselid(self, response):
        return response.css('.at-size-box ::attr(data-varselid)').extract()

    def get_length_varselids(self, response):
        return response.css('.at-size-type-box ::attr(value)').extract()

    def get_length(self, response):
        return response.css('.at-dv-size-type::text').extract_first()

    def get_colours_varselid(self, response):
        return response.css('.color ::attr(data-varselid)').extract()

    def get_colour(self, response):
        return response.css('.at-dv-color::text').extract_first()

    def get_currency(self, response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

    def get_size(self, response):
        return response.css('.at-size-box option[selected="selected"]::text').extract_first().strip()

    def get_is_instock(self, response):
        stock_info = response.css('meta[itemprop="availability"]::attr(content)').extract_first()
        if stock_info:
            if 'InStock' in stock_info:
                return True
            else:
                return False
        return None

    def get_images_url(self, response):
        return response.css('.p-details__image__thumb__container a::attr(href)').extract()

    def get_brand(self, response):
        return response.css('meta[itemprop="manufacturer"]::attr(content)').extract_first()

    def get_name(self, response):
        return response.css('h1[itemprop="name"]::text').extract_first().strip()

    def get_care(self, response):
        return response.css('div.p-details__careSymbols template ::text').extract()

