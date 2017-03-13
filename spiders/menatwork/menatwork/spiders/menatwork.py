import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from menatwork.items import MenatworkItem
import re


class MenatworkSpider(CrawlSpider):
    name = 'menatwork'
    allowed_domains = ['menatwork.nl']
    start_urls = ['http://menatwork.nl/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.search-result-content',)),
             callback='parse_product', follow=True),

        Rule(LinkExtractor(allow=('/nl_NL/dames/', '/nl_NL/heren/')), follow=True),

    )

    seen_ids = set()

    def parse_product(self, response):

        product_id = self.product_id(response)
        if self.processed_products(product_id):
            return None

        product = MenatworkItem()
        product['url'] = response.url
        product['brand'] = self.product_brand(response)
        product['category'] = self.product_category(response)

        description, care = self.product_description_and_care(response)
        product['description'] = description
        product['care'] = care

        product['image_urls'] = self.image_urls(response)
        product['gender'] = self.gender(response)
        product['industry'] = ''
        product['market'] = 'Netherlands'
        product['merch_info'] = []
        product['retailer'] = 'menatwork-nl'
        product['name'] = product['category'][0]
        product['retailer_sku'] = self.product_id(response)

        product_url = self.product_url(response)

        yield scrapy.Request(product_url, callback=self.parse_variants,
                             meta={'product': product})

    def parse_variants(self, response):
        available_sizes = self.variant_sizes_and_availability(response)
        skus = self.get_skus(response, available_sizes)
        response.meta['product']['skus'] = skus

        variants = response.css(".swatches.color > li[class='selectable'] "
                                "> a::attr('href')")
        requests = []
        if not variants:
            yield response.meta['product']
            return

        for variant in variants:
            request = scrapy.Request(variant.extract(), callback=self.parse_colours)
            request.meta['product'] = response.meta['product']
            requests.append(request)

        request = requests.pop()
        request.meta['pending_requests'] = requests
        yield request

    def parse_colours(self, response):
        variants = self.variant_sizes_and_availability(response)
        skus = self.get_skus(response,  variants)
        response.meta['product']['skus'].update(skus)
        requests = response.meta['pending_requests']

        if requests:
            request = requests.pop()
            request.meta['pending_requests'] = requests
            yield request
        else:
            yield response.meta['product']

    def product_url(self, response):
        return response.css('.variation-select option::attr(value)').extract_first()

    def processed_products(self, product_id):
        if product_id in self.seen_ids:
            return True
        else:
            self.seen_ids.add(product_id)
            return False

    def product_id(self, response):
        return response.css('span::attr(data-masterid)').extract_first()

    def product_brand(self, response):
        return response.css('#productData::attr(data-brand)').extract_first()

    def product_category(self, response):
        return response.css('h1.product-name::text').extract()

    def product_description_and_care(self, response):
        description_and_care = response.css('div#tab1::text').extract_first().strip()
        care = r"De stof(.*)\."

        description = re.split(care, description_and_care)[0]
        care = re.findall(care, description_and_care)
        return description, care

    def image_urls(self, response):
        image_urls = response.css('.productthumbnail::attr(src)').extract()
        return [url.replace('small', 'large') for url in image_urls]

    def gender(self, response):
        return response.css('.breadcrumb-element::text').extract_first()

    def construct_sku_id(self, product_id, size, colour):
        return "{0}_{1}_{2}".format(product_id, colour, size)

    def variant_sizes_and_availability(self, response):
        sizes = response.css('.variation-select option::text').extract()
        return [(size.strip(), 'uitverkocht' in size) for size in sizes[1:]]

    def construct_sku(self, response):
        sku = {}
        sku['currency'] = response.css('.price::text').re(r'[A-Z]*')[0]
        sku['colour'] = response.css('.selected-value::text').extract_first()

        parent_class = response.css('.product-price')

        if parent_class.css('.price-standard::text').extract():
            sku['previous_prices'] = parent_class.css('.price-standard::text').extract()

        sku['price'] = parent_class.css('.price-sales::text').extract()
        return sku

    def get_skus(self, response, variants):
        skus = {}
        product_id = self.product_id(response)

        for size, available in variants:
            sku = self.construct_sku(response)
            sku['out_of_stock'] = available
            sku['size'] = size
            sku_id = self.construct_sku_id(product_id, size, sku['colour'])
            skus[sku_id] = sku

        return skus
