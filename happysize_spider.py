import re
from scrapy.spiders import Rule
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from .base import BaseCrawlSpider, BaseParseSpider, clean, reset_cookies
from w3lib.url import url_query_cleaner,url_query_parameter, add_or_replace_parameter, urljoin


class Mixin:
    retailer = 'happysize-de'
    market = 'DE'
    lang = 'de'
    allowed_domains = ['happy-size.de']
    start_urls = ['https://www.happy-size.de']
    out_of_stock_value = '3'
    gender_map = [
        ('damen', 'women'),
        ('herren', 'men'),
        ('men', 'men')
    ]


class HappySizeParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    ajax_api_url = 'AjaxProductDescription?colorId={0}&isAjaxCall=true'
    price_css = 'span.price::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = {}
        garment['trail'] = self.product_trail(response)
        garment['gender'] = self.product_gender(garment)
        garment['image_urls'] = self.product_images(response)

        store_id = clean(response.css('input[name="storeId"]::attr(value)'))[0]

        size_type_requests = self.size_type_requests(response, product_id, store_id)
        size_requests = self.size_requests(response, product_id, store_id)

        requests = size_type_requests or size_requests
        if not requests:
            garment['skus'].update(self.sku(response))

        requests += self.color_requests(response, product_id, store_id)

        if requests:
            garment['meta'] = {'requests_queue': requests}

        return self.next_request_or_garment(garment)

    def color_requests(self, response, product_id, store_id):
        requests = []
        colors = response.css('.color:not(.selected)::attr(title)').extract()
        for color_id in colors:
            color_request_url = response.urljoin(self.ajax_api_url.format(color_id.replace(' ', '+')))
            requests.append(reset_cookies(FormRequest(url=color_request_url, callback=self.parse_color,
                                                      formdata={'productId': product_id, 'storeId': store_id},
                                                      dont_filter=True)))
        return requests

    def parse_color(self, response):
        product_id = self.product_id_from_request(response)
        store_id = self.store_id_from_request(response)

        garment = response.meta['garment']

        size_type_requests = self.size_type_requests(response, product_id, store_id)
        size_requests = self.size_requests(response, product_id, store_id)
        requests = size_type_requests or size_requests

        if requests:
            garment['meta']['requests_queue'] += requests
        else:
            garment['skus'].update(self.sku(response))

        return self.next_request_or_garment(garment)

    def size_type_requests(self, response, product_id, store_id):
        size_types = clean(response.css('#attrId option:not([disabled])::attr(value)'))
        if not size_types:
            return []

        requests = []
        size_type_url = response.url
        color_id = url_query_parameter(response.url, 'colorId')

        if not color_id:
            size_type_url = self.url_with_color_id(response)

        for attr_id in size_types:
            size_type_url = add_or_replace_parameter(size_type_url, 'attrId', attr_id)
            requests.append(reset_cookies(FormRequest(url=size_type_url, callback=self.parse_size_type,
                                                      formdata={'productId': product_id, 'storeId': store_id},
                                                      dont_filter=True)))
        return requests

    def size_requests(self, response, product_id, store_id):
        sizes = clean(response.css('.sizeSelect option:not([disabled])::attr(value)'))
        if not sizes:
            return []

        requests = []
        size_url = response.url

        color_id = url_query_parameter(response.url, 'colorId')
        attr_id = url_query_parameter(response.url, 'attrId', "")

        if not color_id:
            size_url = self.url_with_color_id(response)

        for size_id in sizes:
            size_url = add_or_replace_parameter(size_url, 'attrId', attr_id)
            size_url = add_or_replace_parameter(size_url, 'sizeId', size_id)
            requests.append(reset_cookies(FormRequest(url=size_url, callback=self.parse_size,
                                                      formdata={'productId': product_id, 'storeId': store_id},
                                                      dont_filter=True)))
        return requests

    def parse_size_type(self, response):
        product_id = self.product_id_from_request(response)
        store_id = self.store_id_from_request(response)
        garment = response.meta['garment']
        garment['meta']['requests_queue'] += self.size_requests(response, product_id, store_id)
        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.sku(response))
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('[name="productId"]::attr(value)'))[0]

    def product_name(self, response):
        return clean(response.css('.productName::text'))[0]

    def product_brand(self, response):
        brand = clean(response.css('.brandName::text'))
        return brand[0] if brand else self.retailer

    def product_description(self, response):
        return clean(response.css('[itemprop="description"]::text'))

    def product_care(self, response):
        return clean(response.css('.attributeName::text, .attributeValue::text'))

    def product_category(self, response):
        return clean(response.css('.breadcrumbsEntry [itemprop="title"]::text'))[1:]

    def product_gender(self, garment):
        soup = garment['category'] or [garment['brand']]
        soup = ' '.join(soup).lower()
        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender

        return 'unisex-adults'

    def product_images(self, response):
        return [url_query_cleaner(url).strip('/') for url in clean(response.css('.productThumbNail::attr(src)'))]

    def product_trail(self, response):
        trail_part = [(clean(response.meta.get('link_text', '')), response.url)]
        return response.meta.get('trail', []) + trail_part

    def sku(self, response):
        sku = {}

        color = clean(response.css('input[name="selectedColor"]::attr(value)'))[0]
        size = clean(response.css('input[name="selectedSize"]::attr(value)'))
        if not size:
            size = clean(response.css('.sizeSelect option[selected]::attr(value)'))
        size = size[0] if size else self.one_size

        prices = self.sku_prices(response)

        merch_info = clean(response.css('.salePercentage::text'))

        sku_id = "{0}_{1}".format(color, size)

        sku_stock = clean(response.css('input[name="available"]::attr(value)'))
        if sku_stock:
            sku_stock = False if not sku_stock else False if sku_stock[0] == self.out_of_stock_value else True

        sku[sku_id] = {'color': color, 'size': size, 'in_stock': sku_stock}
        sku[sku_id].update(prices)
        if merch_info:
            sku[sku_id].update({'merch_info': merch_info[0]})

        return sku

    def sku_prices(self, response):
        pprice_string = clean(response.css('span.price.crossedOut::text'))
        price_string = clean(response.css('span.price.reduced::text'))

        if pprice_string and price_string:
            pprice_string = pprice_string[0]
            price_string = price_string[0]
        else:
            pprice_string = ""
            price_string = clean(response.css(self.price_css))[0]

        return self.product_pricing_common_new(response, [price_string, pprice_string])

    def url_with_color_id(self, response):
        color_id = response.css('input[name="colorId"]::attr(value)').extract_first()
        url_color_id = urljoin(response.url, self.ajax_api_url)
        url_color_id = add_or_replace_parameter(url_color_id, 'colorId', color_id)
        return url_color_id.replace('%2B', '+')

    def store_id_from_request(self, response):
        regex = 'storeId=(\d+)'
        return re.findall(regex, str(response.request.body))[0]

    def product_id_from_request(self, response):
        regex = 'productId=(\d+)'
        return re.findall(regex, str(response.request.body))[0]


class HappySizeCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer + '-crawl'
    parse_spider = HappySizeParseSpider()

    category_css = '.categoryNavList'
    product_css = '.catEntryDisplayLink'
    pagination_xpath = '//script[contains(text(), "catalogAjaxURL")]/text()'
    pagination_regex = re.compile('catalogAjaxURL = \"(.*)\";')

    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse_pagination(self, response):

        yield from self.parse(response)

        meta = {'trail': self.add_trail(response)}

        pagination_text = clean(response.xpath(self.pagination_xpath))
        if not pagination_text:
            return

        pagination_url = re.findall(self.pagination_regex, pagination_text[0])[0]
        yield reset_cookies(FormRequest(pagination_url, callback=self.parse_pagination, meta=meta))
