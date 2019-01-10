import json

from w3lib.url import add_or_replace_parameter
from scrapy.spiders import Rule, CrawlSpider, Request
from scrapy.linkextractors import LinkExtractor
from intersport_crawler.items import IntersportCrawlerItem


class intersportcrawler(CrawlSpider):
    GENDER_MAP = {
        'men': 'Men',
        "men's": 'Men',
        'herren': 'Men',
        'herre': 'Men',
        'dam': 'Men',
        'women': 'Women',
        'damen': 'Women',
        'herr': 'Women',
        'boy': 'Boy',
        'jungen': 'Boy',
        'girl': 'Girl',
        'mädchen': 'Girl',
        'kid': 'Unisex-Kids',
        'kinder': 'Unisex-Kids',
        'barn': 'Unisex-Kids'}

    name = 'intersportcrawler'
    allowed_domains = ['intersport.no']
    start_urls = ['https://www.intersport.no/']

    listings_css = ['.navigation']
    products_css = ['.products.wrapper']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_product')
    )

    def parse_pagination(self, response):
        page_size = 20
        page_number = 0
        css = '.product_count_total ::text'
        products = response.css(css).extract_first()
        products = int(products) if products else 0

        for page in range(0, products+1, page_size):
            next_url = add_or_replace_parameter(response.url, 'p', page_number)
            page_number += 1
            yield Request(url=next_url, callback=self.parse)

    def parse_product(self, response):
        item = IntersportCrawlerItem()

        item['lang'] = 'nb'
        item['market'] = 'NB'
        item['url'] = response.url
        item['name'] = self.product_name(response)
        item['skus'] = self.product_skus(response)
        item['brand'] = self.product_brand(response)
        item['category'] = self.product_category(response)
        item['description'] = self.product_description(response)
        item['retailer_sku'] = self.product_id(response)

        if self.product_gender(response):
            item['gender'] = self.product_gender(response)
        if self.product_images_urls(response):
            item['image_urls'] = self.product_images_urls(response)

        return item

    def product_skus(self, response):
        colour_index = 0
        colours = self.product_sizes(response, colour_index)
        return [self.skus(response, c) for c in colours]

    def skus(self, response, colour):
        raw_sku = self.raw_sku(response)
        product_data = raw_sku['ecommerce']['detail']['products']
        sizes = self.product_sizes(response)
        skus = {}
        for size in sizes:
            sku = {'size': size}
            if colour:
                sku['colour']: colour
            if not product_data[0]['quantity']:
                sku['out_of_stock'] = True

            sku['price'] = product_data[0]['price']
            sku['currency'] = raw_sku['ecommerce']['currencyCode']
            skus[f'{self.product_id(response)}_{colour}_{size}'] = sku
        return skus

    def product_images_urls(self, response):
        css = '.mcs-items-container img::attr(src)'
        return response.css(css).extract()

    def product_id(self, response):
        css = '.sku ::text'
        sku_id = response.css(css).extract_first()
        return sku_id.split()[1]

    def product_description(self, response):
        css = '.product.attribute.description > .value::text'
        return response.css(css).extract_first()

    def product_brand(self, response):
        return response.css('.title-brand::text').extract_first()

    def product_name(self, response):
        return response.css('.base::text').extract_first()

    def product_category(self, response):
        raw_sku = self.raw_sku(response)
        list_data = raw_sku['ecommerce']['detail']['products']
        return list_data[0]['category']

    def raw_sku(self, response):
        css = 'script:contains("AEC.Cookie.detail") ::text'
        raw_sku = response.css(css).re_first('AEC.Cookie.detail\(({.*})')
        raw_sku = json.loads(raw_sku)
        return raw_sku

    def product_sizes(self, response, index=1):
        sizes = {}
        css = 'script:contains("AEC.SUPER") ::text'
        raw_product = response.css(css).re_first('AEC.SUPER = (\[.*\])')
        raw_product = json.loads(raw_product)[index]['options']
        for k, v in [(key, d[key]) for d in raw_product for key in d]:
            if k not in sizes:
                sizes[k] = [v]
            else:
                sizes[k].append(v)
        return sizes['label']

    def product_gender(self, response):
        gender_data = response.css('.base::text').extract_first()
        for k, v in self.GENDER_MAP.items():
            if k in gender_data:
                return v
