import scrapy

import w3lib.url

from scrapy.spiders import CrawlSpider

from ..items import OrsayItem


class OrsayParser:

    def parse_details(self, response):
        item = OrsayItem()

        item['retailer_sku'] = self.extract_sku(response)
        item['gender'] = self.extract_gender()
        item['category'] = self.extract_category(response)
        item['brand'] = self.extract_brand()
        item['url'] = self.extract_url(response)
        item['name'] = self.extract_name(response)
        item['description'] = self.extract_description(response)
        item['care'] = self.extract_care(response)
        item['img_urls'] = self.extract_img_url(response)
        item['skus'] = self.extract_skus(response)

        item['request_queue'] = self.extract_color_requests(response)

        yield self.get_item_or_request_to_yield(item)

    def parse_colors(self, response):
        item = response.meta['item']
        item['img_urls'] += self.extract_img_url(response)
        item['skus'] += self.extract_skus(response)

        yield self.get_item_or_request_to_yield(item)

    def get_item_or_request_to_yield(self, item):
        if item['request_queue']:
            request_next = item['request_queue'].pop()
            request_next.meta['item'] = item
            return request_next

        del item['request_queue']
        return item

    def extract_color_requests(self, response):
        colours_urls = response.css('.color [class="selectable"] ::attr(href)').getall()
        return [scrapy.Request(colour_url, callback=self.parse_colors) for colour_url in colours_urls]

    def extract_sku(self, response):
        return response.css('.product-sku::text').get().split()[-1]

    def extract_gender(self):
        return 'Female'

    def extract_category(self, response):
        return self.clean(response.css('.breadcrumb-element-link ::text').getall())

    def extract_brand(self):
        return 'Orsay'

    def extract_url(self, response):
        return response.url

    def extract_name(self, response):
        return response.css('[itemprop="name"]::text').get()

    def extract_description(self, response):
        return response.css('.with-gutter::text').getall()

    def extract_care(self, response):
        return response.css('.js-material-container p::text').getall()

    def extract_img_url(self, response):
        return response.css('.productthumbnail::attr(src)').getall()

    def extract_color(self, response):
        return self.clean(response.css('.color .selected ::attr(title)').get().split('-')[1])

    def extract_pricing_and_color(self, response):
        price = self.clean(response.css('.price-sales::text').get())
        previous_price = self.clean(response.css('.price-standard::text').getall())
        currency = response.css('.locale-item.current .country-currency::text').get()
        color = self.extract_color(response)
        return {'price': price, 'previous_price': previous_price, 'Currency': currency, 'Colour': color}

    def extract_skus(self, response):
        common_sku = self.extract_pricing_and_color(response)
        sizes_sel = response.css('.size li')
        skus = []
        for size_sel in sizes_sel:
            sku = common_sku.copy()
            sku['out_of_stock'] = True if size_sel.css('.unselectable') else False
            sku['size'] = size_sel.css('a::text').get()
            sku['sku_id'] = f"{common_sku['Colour']}_{size_sel.css('a::text').get()}"
            skus.append(sku)
        return skus if skus else common_sku.update({'out_of_stock': False, 'sku_id': common_sku['Colour']})

    def clean(self, list_to_strip):
        if isinstance(list_to_strip, str):
            return list_to_strip.strip()
        return [str_to_strip.strip() for str_to_strip in list_to_strip if str_to_strip.strip()]


class OrsaySpider(CrawlSpider):
    name = "orsay"
    allowed_domains = ['orsay.com']
    start_urls = [
        'https://www.orsay.com/de-de/neuheiten/',
        'https://www.orsay.com/de-de/produkte/',
        'https://www.orsay.com/de-de/sale/',
        'https://www.orsay.com/de-de/trends/',
    ]

    def parse(self, response):
        max_products_on_page = response.css('.load-more-progress::attr(data-max)').get()
        url = w3lib.url.add_or_replace_parameters(response.url, {'sz': max_products_on_page})
        yield response.follow(url, callback=self.parse_category_page)

    def parse_category_page(self, response):
        orsay_parser = OrsayParser()
        for product_url in response.css('.thumb-link::attr(href)'):
            yield response.follow(product_url.get(), callback=orsay_parser.parse_details)


class OrsayItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    img_urls = scrapy.Field()
    skus = scrapy.Field()
    request_queue = scrapy.Field()

