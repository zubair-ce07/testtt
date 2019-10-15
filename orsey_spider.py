import scrapy

from scrapy.spiders import CrawlSpider

from ..items import OrsayItem


class OrsayExtractor:

    def parse_details(self, response):
        orsay_product = OrsayItem()
        orsay_product['retailer_sku'] = self.extract_sku(response)
        orsay_product['gender'] = self.extract_gender()
        orsay_product['category'] = self.extract_category(response)
        orsay_product['brand'] = self.extract_brand()
        orsay_product['url'] = self.extract_url(response)
        orsay_product['name'] = self.extract_name(response)
        orsay_product['description'] = self.extract_description(response)
        orsay_product['care'] = self.extract_care(response)
        orsay_product['img_urls'] = self.extract_img_url(response)
        orsay_product['skus'] = self.extract_skus(response)
        orsay_product['request_queue'] = self.extract_color_requests(response)
        yield self.get_item_or_request_to_yield(orsay_product)

    def parse_colors(self, response):
        orsay_product = response.meta['item']
        orsay_product['img_urls'] += self.extract_img_url(response)
        orsay_product['skus'] += self.extract_skus(response)
        yield self.get_item_or_request_to_yield(orsay_product)

    def get_item_or_request_to_yield(self, orsay_product):
        if orsay_product['request_queue']:
            request_next = orsay_product['request_queue'].pop()
            request_next.meta['item'] = orsay_product
            return request_next
        del orsay_product['request_queue']
        return orsay_product

    def extract_color_requests(self, response):
        colours_urls = response.css('.color [class="selectable"] ::attr(href)').getall()
        return [scrapy.Request(colour_url, callback=self.parse_colors) for colour_url in colours_urls]

    def extract_sku(self, response):
        return response.css('.product-sku::text').get().split()[-1]

    def extract_gender(self):
        return 'Female'

    def extract_category(self, response):
        return [category for category in response.css('.breadcrumb-element-link ::text').getall() if category.strip()]

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

    def extract_price(self, response):
        if response.css('.price-standard').get():
            return response.css('.price-standard::text').get().split(' ')[0].strip()
        return response.css('.price-sales::text').get().split(' ')[0].strip()

    def extract_previous_price(self, response):
        if response.css('.price-standard').get():
            return response.css('.price-sales::text').get().split(' ')[0].strip()
        return ''

    def extract_currency(self, response):
        return response.css('.locale-item.current .country-currency::text').get()

    def extract_color(self, response):
        return response.css('.color .selected ::attr(title)').get().split('-')[1].strip()

    def extract_skus(self, response):
        price = self.extract_price(response)
        previous_price = self.extract_previous_price(response)
        currency = self.extract_currency(response)
        color = self.extract_color(response)
        sizes_list = response.css('.size li')
        skus = []
        if not sizes_list:
            sku = {'Price': price,
                   'previous_price': previous_price,
                   'Currency': currency,
                   'Colour': color,
                   'out_of_stock': 'False',
                   'size': '',
                   'sku_id': color}
            skus.append(sku)
        for size_attr in sizes_list:
            size = size_attr.css('a::text').get().strip()
            out_of_stock = True if size_attr.css('.unselectable') else False
            sku = {'Price': price,
                   'previous_price': previous_price,
                   'Currency': currency,
                   'Colour': color,
                   'out_of_stock': out_of_stock,
                   'size': size,
                   'sku_id': color + "_" + size}
            skus.append(sku)
        return skus


class OrsaySpider(CrawlSpider):
    name = "orsay"
    allowed_domains = ['orsay.com']
    start_urls = [
        'https://www.orsay.com/de-de/neuheiten/',
        'https://www.orsay.com/de-de/produkte/',
        'https://www.orsay.com/de-de/sale/',
        'https://www.orsay.com/de-de/trends/',
        'https://www.orsay.com/de-de/inspiration',
        'https://www.orsay.com/de-de/specials/online-catalog/',
    ]

    def parse(self, response):
        orsay_extraxtor = OrsayExtractor()
        if response.css('.js-next-load'):
            page_size = int(response.css('.load-more-progress-label span::text').get())
            max_pages = int(response.css('.load-more-progress::attr(data-max)').get()) // page_size
            for page in range(1, max_pages):
                url = response.url + '?prefn1=availableMarkets&sz=' + str(page_size) + '&start=' \
                      + str(page_size * page) + '&format=page-element&prefv1=de_DE'
                yield response.follow(url, callback=self.parse)
        for detail_url in response.css('.thumb-link::attr(href)'):
            yield response.follow(detail_url.get(), callback=orsay_extraxtor.parse_details)



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

