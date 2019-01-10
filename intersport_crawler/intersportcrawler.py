import json

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

    listing_css = ['.navigation']
    product_css = ['.products.wrapper']
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product')
    )

    def parse_pagination(self, response):
        total_products = self.parse_products_count(response)
        PRODUCTS_PER_PAGE = 20
        page_number = 0
        for page in range(0, total_products+1, PRODUCTS_PER_PAGE):
            next_url = response.url + '?p=' + str(page_number)
            page_number += 1
            yield Request(url=next_url, callback=self.parse)

    def parse_products_count(self, response):
        total_product_css = '.product_count_total ::text'
        products = response.css(total_product_css).extract_first()
        return int(products) if products else 0

    def parse_product(self, response):
        item = IntersportCrawlerItem()
        item['brand'] = self.product_brand(response)
        item['category'] = self.product_category(response)
        item['description'] = self.product_description(response)
        gender = self.product_gender(response)
        if gender:
            item['gender'] = gender
        imgs_urls = self.product_images_urls(response)
        if imgs_urls:
            item['image_urls'] = imgs_urls
        item['lang'] = 'nb'
        item['market'] = 'NB'
        item['name'] = self.product_name(response)
        item['retailer_sku'] = self.product_id(response)
        item['url'] = response.url
        item['skus'] = self.product_skus(response)
        return item

    def product_skus(self, response):
        skus = {}
        colour_index = 0
        colours = self.product_sizes(response, colour_index)
        for colour in colours:
            skus.update(self.skus(response, colour))
        return skus

    def skus(self, response, colour):
        json_data = self.product_raw_data(response)
        product_data = json_data['ecommerce']['detail']['products']
        sizes = self.product_sizes(response)
        skus = {}
        for size in sizes:
            sku = {}
            if colour:
                sku['colour']: colour
            if not product_data[0]['quantity']:
                sku['out_of_stock'] = product_data[0]['quantity']
            sku['currency'] = json_data['ecommerce']['currencyCode']
            sku['price'] = product_data[0]['price']
            sku['size'] = size
            skus[f'{self.product_id(response)}_{size}'] = sku
        return skus

    def product_images_urls(self, response):
        css = '.mcs-items-container img::attr(src)'
        return response.css(css).extract()

    def product_id(self, response):
        care_css = '.sku ::text'
        sku_id = response.css(care_css).extract_first()
        return sku_id.split()[1]

    def product_description(self, response):
        css = '.product.attribute.description > .value::text'
        return response.css(css).extract_first()

    def product_brand(self, response):
        return response.css('.title-brand::text').extract_first()

    def product_name(self, response):
        return response.css('.base::text').extract_first()

    def product_raw_data(self, response):
        css = 'script:contains("AEC.Cookie.detail") ::text'
        raw_skus = response.css(css).re_first('AEC.Cookie.detail\(({.*})')
        raw_skus = json.loads(raw_skus)
        return raw_skus

    def product_category(self, response):
        raw_data = self.product_raw_data(response)
        list_data = raw_data['ecommerce']['detail']['products']
        return list_data[0]['category']

    def product_sizes(self, response, index=1):
        sizes = {}
        css = 'script:contains("AEC.SUPER") ::text'
        raw_data = response.css(css).re_first('AEC.SUPER = (\[.*\])')
        json_data = json.loads(raw_data)[index]['options']
        for k, v in [(key, d[key]) for d in json_data for key in d]:
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
