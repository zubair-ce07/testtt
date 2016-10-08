from urllib.parse import urlparse, urljoin, parse_qs, urlsplit, urlencode
import itertools
from scrapy import FormRequest, Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from wittweiden.items import GarmentItem
import re
import json
import copy


class WittWeidenSpider(CrawlSpider):
    name = 'witt_weiden_spider'
    allowed_domains = ['witt-weiden.de']
    start_urls = ['http://www.witt-weiden.de']
    witt_base_url = 'http://www.witt-weiden.de/'
    rules = (
        Rule(LinkExtractor(restrict_css=["a.osecom-navbar__category-link",
                                         "a.next"]),
             callback="parse_item_grid"),)

    def parse_item_grid(self, response):
        garment_item = GarmentItem()
        garment_item['trail'] = [self.witt_base_url]
        garment_item['trail'].append(response.url)
        for url in response.css('article> div.image> a::attr(href)').extract():
            yield Request(url, meta={'item': copy.deepcopy(garment_item)},
                          callback=self.parse_item)

    def parse_item(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        garment_item = response.meta['item']
        garment_model_number = self.garment_model_number(response)
        garment_item['url'] = response.url
        garment_item['trail'].append(response.url)
        garment_item['retailer_sku'] = garment_model_number
        garment_item['gender'] = self.garment_gender(garment_item['url'])
        garment_item['description'] = self.garment_description(response)
        yield self.xhr_request(
            "http://www.witt-weiden.de/ajax/product-detail/article-header.html",
            callback=self.parse_garment_meta,
            query_params={'modelNumber': garment_model_number},
            meta={'model_number': garment_model_number, 'item': garment_item})

    def parse_garment_meta(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        model_number = response.meta['model_number']
        garment_item = response.meta['item']
        garment_item['name'] = self.garment_name(response)
        garment_item['market'] = 'Germany'
        garment_item['retailer'] = 'Witt Weiden'
        garment_item['spider_name'] = self.name
        garment_item['brand'] = 'Witt Weiden'
        yield self.xhr_request(
            "http://www.witt-weiden.de/ajax/product-detail/main-image.html",
            query_params={'modelNumber': model_number},
            callback=self.parse_garment_default_image,
            meta={'item': garment_item, 'model_number': model_number})

    def parse_garment_default_image(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        model_number = response.meta['model_number']
        garment_item = response.meta['item']
        garment_item['image_urls'] = set(self.garment_default_image(response))
        yield self.xhr_request(
            "http://www.witt-weiden.de/ajax/product-detail/color-images.html",
            query_params={'modelNumber': model_number},
            callback=self.parse_garment_color_images,
            meta={'item': garment_item, 'model_number': model_number})

    def parse_garment_color_images(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        model_number = response.meta['model_number']
        garment_item = response.meta['item']
        garment_item['image_urls'].update(self.garment_image_urls(response))
        yield self.xhr_request(
            "http://www.witt-weiden.de/ajax/product-detail/description-table.html",
            query_params={'modelNumber': model_number},
            callback=self.parse_garment_details,
            meta={'model_number': model_number, 'item': garment_item})

    def parse_garment_details(self, response):
        """For a given item url response, populates the available
        garment information and yields the final item"""
        garment_item = response.meta['item']
        garment_item['care'] = self.garment_care(response)
        model_number = response.meta['model_number']
        yield self.xhr_request(
            "http://www.witt-weiden.de/ajax/product-detail/buy-box.html",
            callback=self.parse_garment_price_box,
            query_params={'modelNumber': model_number},
            meta={'model_number': model_number, 'item': garment_item})

    def parse_garment_price_box(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        garment_item = response.meta['item']
        garment_item['currency'] = 'EUR'
        skus_requests = self.sku_requests(response)
        response.meta['item'] = garment_item
        response.meta['remaining_sku_requests'] = skus_requests
        response.meta['remaining_img_requests'] = copy.deepcopy(skus_requests)
        response.meta['skus'] = {}
        yield self.parse_garment_sku(response)

    def parse_garment_sku(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        color_variant = self.get_query_value(response.url, 'articleNumber')
        article_size = self.get_query_value(response.url, 'size')
        model_number = response.meta['model_number']
        sku_key = model_number
        sku_key += color_variant if color_variant else ''
        sku_key += article_size if article_size else ''
        garment_item = response.meta['item']
        skus = response.meta['skus']
        sku = self.garment_sku(response)
        if sku:
            skus[sku_key] = sku
        updated_meta = response.meta
        updated_meta['item'] = garment_item
        updated_meta['skus'] = skus
        updated_meta['model_number'] = model_number
        return self.next_sku_request(meta=updated_meta)

    def next_sku_request(self, meta={}):
        model_number = meta['model_number']
        remaining_requests = meta['remaining_sku_requests']
        if remaining_requests:
            sku_request = remaining_requests.pop()
            meta['remaining_sku_requests'] = remaining_requests
            return self.xhr_request(
                'http://www.witt-weiden.de/ajax/product-detail/buy-box.html',
                callback=self.parse_garment_sku,
                query_params={
                    'modelNumber': model_number,
                    'size': sku_request.get('size'),
                    'articleNumber': sku_request.get('articleNumber')
                },
                meta=meta)
        else:
            meta['item']['skus'] = meta['skus']
            return self.next_img_request(meta=meta)

    def next_img_request(self, meta={}):
        model_number = meta['model_number']
        remaining_requests = meta['remaining_img_requests']
        if remaining_requests:
            img_requests = remaining_requests.pop()
            meta['remaining_img_requests'] = remaining_requests
            return self.xhr_request(
                "http://www.witt-weiden.de/ajax/product-detail/inspection-images.html",
                callback=self.parse_garment_inspection_images,
                query_params={
                    'modelNumber': model_number,
                    'size': img_requests.get('size'),
                    'articleNumber': img_requests.get('articleNumber')},
                meta=meta)
        else:
            meta['item']['image_urls'] = list(meta['item']['image_urls'])
            return meta['item']

    def parse_garment_inspection_images(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        garment_item = response.meta['item']
        garment_item['image_urls'].update(self.garment_image_urls(response))
        response.meta['item'] = garment_item
        updated_meta = response.meta
        updated_meta['item'] = garment_item
        yield self.next_img_request(meta=response.meta)

    def sku_requests(self, response):
        garment_sizes = self.garment_sizes(response)
        color_variants = self.garment_color_variants(response)
        skus_requests = [dict(zip(['articleNumber', 'size'], prod)) for prod
                         in itertools.product(color_variants, garment_sizes)]
        if not skus_requests:
            if garment_sizes:
                skus_requests = [{'size': size} for size in garment_sizes]
            if color_variants:
                skus_requests = [{'articleNumber': color} for color in
                                 color_variants]
        return skus_requests

    def get_query_value(self, url, query_name):
        queries = parse_qs(urlsplit(url).query)
        query_value = queries.get(query_name)
        return query_value[0] if query_value else None

    def garment_attr_value(self, url, attr):
        search_result = re.search(r'%s=?([0-9A-z]*)' % attr, url)
        if search_result:
            return search_result.group(1)

    def garment_color_variants(self, response):
        garment_color_urls = response.css(
            "#color-control-group ul a::attr(href)").extract()
        return [self.garment_attr_value(color_url, 'articleNumber') for
                color_url in garment_color_urls]

    def garment_sizes(self, response):
        """ Returns all available sizes of a garment """
        garment_color_urls = response.css(
            "#size-control-group ul a::attr(href)").extract()
        return [self.garment_attr_value(size_url, '#size') for
                size_url in garment_color_urls if size_url != '#']

    def xhr_request(self, url, **kwargs):
        """ Returns a new XHR request"""
        filtered_query_params = {k: v for (k, v) in kwargs[
            'query_params'].items()
                                 if v}
        return FormRequest(url=url,
                           formdata=filtered_query_params,
                           callback=kwargs['callback'], method='GET',
                           meta=kwargs['meta'],
                           headers={'X-Requested-With': 'XMLHttpRequest'})

    def garment_model_number(self, response):
        """ Returns model number of a garment """
        garment_detail_json = json.loads(response.css(
            'section#product-detail::attr(data-product)').extract_first())
        return garment_detail_json['modelNumber']

    def garment_default_image(self, response):
        """ Returns the default zoomed image of the current garment """
        return [response.urljoin(response.css('#desktopZoom ''img::attr(src)').
                                 extract_first().replace('5.jpg', '9.jpg'))]

    def garment_name(self, response):
        """ Returns the name of the current garment """
        return response.css('header> h1::text').extract_first()

    def garment_description(self, response):
        description = response.css('#description-text> p::text').extract()
        description.extend(response.css('#description-text> p font'
                                        '::text').extract())
        return description

    def garment_care(self, response):
        """ Returns the care instructions of the current garment """
        return response.xpath(
            "//tr/th[contains(text(), 'Pflege:')]/parent::tr/td/text()"
        ).extract_first()

    def garment_gender(self, garment_url):
        """ Returns the gender of the garment """
        if 'herren' in garment_url:
            return 'Boys'
        if 'damen' in garment_url:
            return 'Girls'
        return 'Universal'

    def garment_image_urls(self, response):
        """ Returns the urls of all garment colors """
        return [response.urljoin(img_url).replace('4.jpg', '9.jpg')
                for img_url in response.css("a img::attr(src)").extract()]

    def garment_price(self, response):
        """ Returns the price of the current garment """
        price_components = response.css("#article-price> p.price>strong "
                                        "*::text").extract()
        current_price = ''.join(price_components)
        prev_price = response.css("#article-price> p.price> strike::text") \
            .extract_first()
        return {'current_price': current_price, 'prev_price': prev_price}

    def garment_sku(self, response):
        """ Returns a SKU of the current garment """
        garment_out_of_stock = True if response.css(
            "#submitButton.disabled") else False
        garment_color = response.css(
            "input#color::attr(value)").extract_first()
        garment_size = response.css("input#size::attr(value)").extract_first()
        if garment_size != '-':
            return {'colour': garment_color, 'currency': 'EUR',
                    'out_of_stock': garment_out_of_stock, 'size': garment_size,
                    'prices': self.garment_price(response)}
