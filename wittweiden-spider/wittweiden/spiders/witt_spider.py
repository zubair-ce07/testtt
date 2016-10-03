from urllib.parse import urlparse, urlencode, urljoin
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from wittweiden.items import GarmentItem
import re
import json


class WittWeidenSpider(CrawlSpider):
    name = 'witt_weiden_spider'
    allowed_domains = ['witt-weiden.de']
    start_urls = ['http://www.witt-weiden.de/']
    witt_base_url = 'http://www.witt-weiden.de/'

    rules = (
        Rule(LinkExtractor(restrict_css=["a.osecom-navbar__category-link",
                                         "a.next"])),
        Rule(LinkExtractor(restrict_css="article> div.image> a"),
             callback='parse_sale_item')
    )

    def parse_sale_item(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        garment_item = GarmentItem()
        garment_model_number = self.garment_model_number(response)
        garment_item['url'] = self.garment_url(response)
        garment_item['trail'] = self.garment_url_trail(garment_item['url'])
        garment_item['retailer_sku'] = garment_model_number
        garment_item['gender'] = self.garment_gender(garment_item['url'])
        yield self.create_xhr_request("/article-header.html",
                                      query_params={
                                          'modelNumber': garment_model_number},
                                      callback=self.parse_garment_header,
                                      meta={
                                          'model_number': garment_model_number,
                                          'item': garment_item})

    def parse_garment_header(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        model_number = response.meta['model_number']
        garment_item = response.meta['item']
        garment_item['name'] = self.garment_name(response)
        garment_item['market'] = self.garment_market()
        garment_item['retailer'] = self.garment_retailer()
        garment_item['spider_name'] = self.spider_name()
        garment_item['brand'] = self.garment_brand()
        yield self.create_xhr_request(
            "/buy-box.html",
            query_params={'modelNumber': model_number},
            callback=self.parse_garment_price_box,
            meta={'model_number': model_number,
                  'item': garment_item})

    def parse_garment_price_box(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        garment_item = response.meta['item']
        garment_item['currency'] = self.garment_currency()
        garment_sizes = self.garment_sizes(response)
        garment_articles = self.garment_articles(response)

        skus_requests = []
        if not garment_articles:
            skus_requests = [{'size': size} for size in garment_sizes]
        if not garment_sizes:
            skus_requests = [{'articleNumber': article} for article in
                             garment_articles]

        for article in garment_articles:
            for size in garment_sizes:
                skus_requests.append({
                    'articleNumber': article,
                    'size': size
                })

        response.meta['item'] = garment_item
        response.meta['remaining_requests'] = skus_requests
        response.meta['skus'] = {}
        response.meta['garment_articles'] = garment_articles

        yield self.parse_garment_sku(response)

    def parse_garment_sku(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        article_number = self.get_query_value(response.url, 'articleNumber')
        article_size = self.get_query_value(response.url, 'size')

        model_number = response.meta['model_number']
        sku_key = model_number
        sku_key += article_number if article_number else ''
        sku_key += article_size if article_size else ''

        garment_item = response.meta['item']
        skus = response.meta['skus']
        sku = self.garment_sku(response)
        if sku:
            skus[sku_key] = sku
        skus_requests = response.meta['remaining_requests']

        if skus_requests:
            sku_request = skus_requests.pop()
            return self.create_xhr_request(
                '/buy-box.html',
                query_params={
                    'modelNumber': model_number,
                    'size': sku_request['size'] if 'size' in sku_request
                    else None,
                    'articleNumber': sku_request['articleNumber'] if
                    'articleNumber' in sku_request else None
                },
                callback=self.parse_garment_sku,
                meta={'item': garment_item,
                      'remaining_requests': skus_requests,
                      'model_number': model_number,
                      'skus': skus})
        else:
            garment_item['skus'] = skus

            return self.create_xhr_request(
                "/color-images.html",
                query_params={'modelNumber': model_number},
                callback=self.parse_garment_color_images,
                meta={'item': garment_item,
                      'model_number': model_number})

    def parse_garment_color_images(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        model_number = response.meta['model_number']
        garment_item = response.meta['item']
        garment_item['image_urls'] = self.garment_image_url(response)
        yield self.create_xhr_request(
            "/inspection-images.html",
            query_params={'modelNumber': model_number},
            callback=self.parse_garment_backview_images,
            meta={'model_number': model_number,
                  'item': garment_item})

    def parse_garment_backview_images(self, response):
        """For a given item url response, populates the available
        garment information and creates succeeding request"""
        model_number = response.meta['model_number']
        garment_item = response.meta['item']
        garment_item['image_urls'].extend(self.garment_image_url(response))
        yield self.create_xhr_request("/description-table.html",
                                      query_params={
                                          'modelNumber': model_number},
                                      callback=self.parse_garment_details,
                                      meta={'model_number': model_number,
                                            'item': garment_item})

    def parse_garment_details(self, response):
        """For a given item url response, populates the available
        garment information and yields the final item"""
        garment_item = response.meta['item']
        garment_item['description'] = self.garment_description(response)
        yield garment_item

    def get_query_value(self, url, query):
        search_obj = re.search(r'(?<=' + query + '=)[0-9a-zA-Z]+', url)
        if search_obj:
            return search_obj.group()

    def garment_articles(self, response):
        garment_color_urls = response.css(
            "#color-control-group ul a::attr(href)").extract()
        return [self.get_query_value(color_url, 'articleNumber') for
                color_url in garment_color_urls]

    def garment_sizes(self, response):
        """ Returns all available sizes of a garment """
        garment_color_urls = response.css(
            "#size-control-group ul a::attr(href)").extract()
        return [self.get_query_value(size_url, 'size') for
                size_url in garment_color_urls if size_url != '#']

    def create_xhr_request(self, endpoint, callback=None, meta={},
                           query_params={}):
        """ Returns a new XHR request"""
        url = "http://www.witt-weiden.de/ajax/product-detail" + \
              endpoint + '?' + urlencode(query_params)
        return Request(url, callback=callback, meta=meta, headers={
            'X-Requested-With': 'XMLHttpRequest'})

    def garment_model_number(self, response):
        """ Returns model number of a garment """
        garment_detail_json = json.loads(response.css(
            'section#product-detail::attr(data-product)').extract_first())
        return garment_detail_json['modelNumber']

    def spider_name(self):
        """ Returns the name of the current spider """
        return self.name

    def garment_url(self, response):
        """ Returns the url the current http response """
        return response.url

    def garment_name(self, response):
        """ Returns the name of the current garment """
        return response.css('header> h1::text').extract_first()

    def garment_brand(self):
        """ Returns the name of brand """
        return 'Witt Weiden'

    def garment_currency(self):
        """ Returns the currency being used """
        return "Euro"

    def garment_description(self, response):
        """ Returns the description of the current garment """
        description = {
            'care': response.xpath("//tr/th[contains(text(),"
                                   "'Pflege:')]/parent::tr/td/text()"
                                   ).extract_first(),
            'material': response.xpath("//tr/th[contains(text(),"
                                       "'Material')]/parent::tr/td/text()"
                                       ).extract_first(),
        }
        return description

    def garment_gender(self, garment_url):
        """ Returns the gender of the garment """
        if 'herren' in garment_url:
            return 'Boys'
        if 'damen' in garment_url:
            return 'Girls'
        return 'Universal'

    def garment(self, response):
        """ Returns json object that has all the relevant product
        information in the webpage """
        js_element = response.xpath("//head/script[contains("
                                    "text(), 'var dataobj')]").extract_first()
        garment_found = re.search('var dataobj = (.+?);\n', js_element)
        garment_info_json = garment_found.group(1)
        return json.loads(garment_info_json)['product']

    def garment_image_url(self, response):
        """ Returns the urls of all garment colors """
        return [urljoin(self.witt_base_url, img_url) for img_url in \
                response.css("a img::attr(src)").extract()]

    def garment_market(self):
        """ Returns the market name """
        return 'Germany'

    def garment_price(self, response):
        """ Returns the price of the current garment """
        current_price = response.css(
            "#article-price> p.price> strong::text").extract_first()
        current_price += response.css("#article-price> p.price> strong> "
                                      "sup::text").extract_first()
        prev_price = response.css(
            "#article-price> p.price> strike::text").extract_first()
        return {'current_price': current_price, 'prev_price': prev_price}

    def garment_retailer(self):
        """ Returns the retailer of the current garment """
        return 'Witt Weiden'

    def garment_sku(self, response):
        """ Returns a SKU of the current garment """
        garment_out_of_stock = True if response.css(
            "#submitButton.disabled").extract_first() else False
        garment_color = response.css("input#color::attr("
                                     "value)").extract_first()
        garment_size = response.css("input#size::attr(value)").extract_first()
        if garment_size != '-':
            return {'colour': garment_color,
                    'currency': 'Euros',
                    'out_of_stock':
                        garment_out_of_stock,
                    'prices': self.garment_price(
                        response),
                    'size': garment_size}

    def garment_url_trail(self, url):
        """ Returns the navigation trail of the current garment """
        parsed_url = urlparse(url)
        return [parsed_url.netloc, parsed_url.path]
