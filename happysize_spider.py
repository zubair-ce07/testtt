import re
from scrapy.spiders import Rule
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from .base import BaseCrawlSpider, BaseParseSpider, clean, reset_cookies
from w3lib.url import url_query_cleaner,url_query_parameter, add_or_replace_parameter, urljoin


class Mixin:
    retailer = 'happy-size-de'
    market = 'DE'
    lang = 'de'
    allowed_domains = ['happy-size.de']
    start_urls = ['https://www.happy-size.de']
    gender_map = [
        ('damen', 'women'),
        ('herren', 'men'),
        ('men', 'men')
    ]


class HappySizeParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    ajax_api_url = 'AjaxProductDescription?colorId={0}&isAjaxCall=true'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        requests = []
        garment['skus'] = {}
        garment['gender'] = self.product_gender(garment)
        garment['image_urls'] = self.product_images(response)
        garment['trail'] = self.product_trail(response, garment['name'])

        store_id, types, sizes = self.product_meta(response)

        if types:
            requests = self.type_or_size_request(response, product_id, store_id, types, "Type")
        if sizes:
            requests = self.type_or_size_request(response, product_id, store_id, sizes, "Size")
        if not types and not sizes:
            garment['skus'].update(self.sku(response))

        requests += self.color_request(response, product_id, store_id)

        garment['meta'] = {'requests_queue': requests}

        return self.next_request_or_garment(garment)

    def color_request(self, response, product_id, store_id):
        requests = []
        colors = response.css('.color:not(.selected)::attr(title)').extract()
        for color_id in colors:
            color_request_url = response.urljoin(self.ajax_api_url.format(color_id.replace(' ', '+')))
            requests.append(reset_cookies(FormRequest(url=color_request_url, callback=self.parse_color,
                                                      formdata={'productId': product_id, 'storeId': store_id},
                                                      dont_filter=True)))
        return requests

    def parse_color(self, response):
        requests = []
        product_id, store_id = self.ids_from_request(response)
        garment = response.meta['garment']

        _, types, sizes = self.product_meta(response)
        if types:
            requests = self.type_or_size_request(response, product_id, store_id, types, "Type")
        if sizes:
            requests = self.type_or_size_request(response, product_id, store_id, sizes, "Size")

        if requests:
            garment['meta']['requests_queue'] += requests
        else:
            garment['skus'].update(self.sku(response))

        return self.next_request_or_garment(garment)

    def type_or_size_request(self, response, product_id, store_id, type_or_sizes, filter):
        if not type_or_sizes:
            return []

        requests = []
        type_or_size_request_url = response.url

        color_id = url_query_parameter(response.url, 'colorId')
        type = url_query_parameter(response.url, 'attrId')
        callback = self.parse_type if filter == "Type" else self.parse_size

        if not color_id:
            color_id = response.css('input[name="colorId"]::attr(value)').extract_first()
            type_or_size_request_url = urljoin(response.url, self.ajax_api_url)
            type_or_size_request_url = add_or_replace_parameter(type_or_size_request_url, 'colorId', color_id)
            type_or_size_request_url.replace('%2B', '+')

        url = type_or_size_request_url

        for type_or_size in type_or_sizes:
            url = add_or_replace_parameter(url, 'attrId', type_or_size if filter == "Type" else type if type else "")
            url = add_or_replace_parameter(url, 'sizeId', type_or_size if filter == "Size" else "")
            requests.append(reset_cookies(FormRequest(url=type_or_size_request_url, callback=callback,
                                                      formdata={'productId': product_id, 'storeId': store_id},
                                                      dont_filter=True)))
        return requests

    def parse_type(self, response):
        product_id, store_id = self.ids_from_request(response)
        garment = response.meta['garment']
        _, _, sizes = self.product_meta(response)
        garment['meta']['requests_queue'] += self.type_or_size_request(response, product_id, store_id, sizes, "Size")
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

    def product_trail(self, response, name):
        trail_part = [(clean(name), response.url)]
        return response.meta.get('trail', []) + trail_part

    def sku(self, response):
        sku = {}
        out_of_stock_value = 3
        color, size = self.sku_color_size(response)
        prices = self.sku_prices(response)

        merch_info = clean(response.css('.salePercentage::text'))

        sku_id = "_".join([color, size])

        sku_stock = clean(response.css('input[name="available"]::attr(value)'))
        if sku_stock:
            sku_stock = False if sku_stock == out_of_stock_value else True
        else:
            sku_stock = False

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
            price_string = clean(response.css('span.price::text'))[0]

        return self.product_pricing_common_new(response, [price_string, pprice_string])

    def sku_color_size(self, response):
        selected_color = clean(response.css('input[name="selectedColor"]::attr(value)'))[0]
        selected_size = clean(response.css('input[name="selectedSize"]::attr(value)'))

        if not selected_size:
            selected_size = clean(response.css('.sizeSelect option[selected]::attr(value)'))

        selected_size = selected_size[0] if selected_size else self.one_size
        return selected_color, selected_size

    def product_meta(self, response):
        store_id = clean(response.css('input[name="storeId"]::attr(value)'))
        types = clean(response.css('#attrId option:not([disabled])::attr(value)'))
        sizes = clean(response.css('.sizeSelect option:not([disabled])::attr(value)'))
        return store_id[0] if store_id else "", types, sizes

    def ids_from_request(self, response):
        color_store_regex = 'productId=(\d+)&storeId=(\d+)|storeId=(\d+)&productId=(\d+)'
        ids = re.findall(color_store_regex, str(response.request.body))[0]
        product_id = ids[0] if ids[0] else ids[3]
        store_id = ids[1] if ids[1] else ids[2]
        return product_id, store_id


class HappySizeCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer + '-crawl'
    parse_spider = HappySizeParseSpider()

    category_css = '.categoryNavList'
    product_css = '.catEntryDisplayLink'

    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse_pagination(self, response):

        yield from self.parse(response)

        meta = {'trail': self.add_trail(response)}

        pagination_xpath = '//script[contains(text(), "catalogAjaxURL")]/text()'
        pagination_text = clean(response.xpath(pagination_xpath))
        if not pagination_text:
            return

        pagination_url = re.findall('catalogAjaxURL = \"(.*)\";', pagination_text[0])[0]
        yield reset_cookies(FormRequest(pagination_url, callback=self.parse_pagination, meta=meta))
