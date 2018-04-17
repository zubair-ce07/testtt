import json
import re
from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from alexanderwang_scrapy.items import Product


class AlexanderWangSpider(CrawlSpider):

    name = "alexanderwang"
    allowed_domains = ['alexanderwang.com']
    start_urls = ['https://www.alexanderwang.com/us']
    ids_seen = []

    deny_re = ['_section', 'studio']

    listings_css = "nav.mainMenu"
    products_css = "a.title"

    gender_map = ([
        ('women', 'women'),
        ('men', 'men'),
        ('girls', 'girls'),
        ('boys', 'boys'),
        ('kids', 'unisex-kids')
    ])

    rules = (
        Rule(LinkExtractor(
            restrict_css=listings_css,
            deny=deny_re),
             callback='parse_pagination',
             follow=True
            ),
        Rule(LinkExtractor(
            restrict_css=products_css,
            deny=deny_re),
             callback='parse_product'
            ),
    )

    def parse_pagination(self, response):
        scripts = response.css('script ::text')
        parameters = json.loads(scripts.re_first(r'yTos.search = (.+?);'))
        total_pages = parameters['totalPages']
        for page_number in range(1, int(total_pages) + 1):
            products_list_url = response.urljoin('?page={}'.format(page_number))
            yield Request(products_list_url, callback=self.parse)

    def parse_product(self, response):
        sold = response.css('div.soldOutMessage')
        if sold:
            return

        full_id = self.product_retailer_sku(response)
        retailer_sku = full_id[0]
        if retailer_sku in self.ids_seen:
            return

        self.ids_seen.append(retailer_sku)
        product = Product()
        product['retailer_sku'] = retailer_sku
        product['name'] = self.product_name(response)
        product['brand'] = self.product_brand(response)
        product['url'] = response.url.split('?')[0]
        product['category'] = self.product_category(response, product['name'])
        product['gender'] = self.product_gender(product['category'])
        product['description'] = self.product_description(response)
        product['image_urls'] = self.product_images(response)

        price = self.product_price(response)
        currency = self.product_currency(response)
        skus_url = response.urljoin('/yTos/api/Plugins/ItemPluginApi/GetCombinationsAsync/?site'
                                    'Code=ALEXANDERWANG_US&code10={}'.format(''.join(full_id)))

        skus_request = Request(skus_url, callback=self.parse_skus)
        skus_request.meta['product'] = product
        skus_request.meta['price'] = price
        skus_request.meta['currency'] = currency
        yield skus_request

    def parse_skus(self, response):
        product = response.meta['product']
        price = response.meta['price']
        currency = response.meta['currency']
        product['skus'], additional_color_urls = self.product_skus(response, product['url'],
                                                                   price, currency)

        if additional_color_urls:
            images_request = Request(additional_color_urls.pop(0), callback=self.parse_images)
            images_request.meta['product'] = product
            request_queue = []
            for color_url in additional_color_urls:
                request = Request(color_url, callback=self.parse_images)
                request_queue.append(request)
            images_request.meta['request_queue'] = request_queue
            yield images_request
        else:
            yield product

    def parse_images(self, response):
        product = response.meta['product']
        requests = response.meta['request_queue']
        product['image_urls'] += self.product_images(response)

        if requests:
            request = requests.pop(0)
            request.meta['product'] = product
            request.meta['request_queue'] = requests
            yield request
        else:
            yield product

    @staticmethod
    def product_skus(response, product_url, price, currency):
        product_skus = json.loads(response.text)
        skus = []
        additional_color_urls = []
        for product_sku in product_skus['ModelColorSizes']:
            sku = {}
            sku['price'] = price
            sku['currency'] = currency
            sku['colour'] = product_sku['Color']['Description']
            sku['size'] = product_sku['Size']['Description']
            sku['sku_id'] = '{}_{}'.format(sku['colour'], sku['size'])
            skus.append(sku)

            color_url = product_sku['Color']['Link']
            if color_url != product_url and color_url not in additional_color_urls:
                additional_color_urls.append(color_url)
        return skus, additional_color_urls

    @staticmethod
    def product_images(response):
        return response.css('div#itemImages img::attr(src)').extract()

    @staticmethod
    def product_retailer_sku(response):
        scripts = response.css('script ::text')
        return scripts.re(r'"Code10":"(\d+)(.+?)"')

    @staticmethod
    def product_brand(response):
        brand = response.css('body').re_first('productBrand":"(.*?)"')
        if not brand:
            brand = response.css('body').re_first('productBrand&quot;:&quot;(.*?)&quot;')
        if brand:
            return brand.title()
        else:
            return 'Alexander Wang'

    @staticmethod
    def product_name(response):
        name = response.css('h1.productName span.modelName::text').extract_first()
        return clean(name.title())

    @staticmethod
    def product_category(response, name):
        keywords = response.css("meta[name='keywords']::attr(content)").extract_first()
        keywords = clean(keywords.split(','))
        category = []
        for keyword in keywords:
            if keyword.lower() != 'alexander wang' and keyword.lower() != name.lower():
                category.append(keyword)
        category.reverse()
        return [c.title() for c in category]

    def product_gender(self, categories):
        for category in categories:
            for gender_key, gender_value in self.gender_map:
                if gender_key in category.lower():
                    return gender_value
        return 'unisex-adults'

    @staticmethod
    def product_description(response):
        desc = response.css('div.ItemDescription span.text::text').extract()
        return clean(desc)

    @staticmethod
    def product_price(response):
        price = response.css('div.itemBoxPrice span.value::text').extract_first()
        return int(float(price.replace(',', '')) * 100)

    @staticmethod
    def product_currency(response):
        return response.css('script::text').re_first(r'"priceCurrency": "(.+?)"')


def clean(formatted):
    if not formatted:
        return formatted
    if isinstance(formatted, list):
        cleaned = [re.sub(r'\s+', ' ', each).strip() for each in formatted]
        return list(filter(None, cleaned))
    return re.sub(r'\s+', ' ', formatted).strip()
