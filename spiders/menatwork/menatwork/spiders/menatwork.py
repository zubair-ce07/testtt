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

    processed_pids = set()

    def parse_product(self, response):

        product_id = self.product_id(response)
        if self.processed_products(product_id):
            return None

        product = MenatworkItem()
        product['url'] = response.url
        product['brand'] = self.product_brand(response)
        product['category'] = self.product_category(response)

        description_and_care = self.product_description_and_care(response)
        product['description'] = [description_and_care[0]]
        product['care'] = [description_and_care[1] if
                           len(description_and_care) > 1 else None]

        product['image_urls'] = self.image_urls(response)
        product['gender'] = self.gender(response)
        product['industry'] = ''
        product['market'] = 'Netherlands'
        product['merch_info'] = []
        product['retailer'] = 'menatwork-nl'

        product['name'] = product['category'][0]
        product['retailer_sku'] = self.product_id(response)

        product_start_url = self.product_start_link(response)

        yield scrapy.Request(product_start_url, callback=self.parse_variants,
                             meta={'product': product})

    def parse_variants(self, response):
        variants = self.variant_sizes_and_availability(response)
        skus = self.get_skus(response, variants)
        response.meta['product']['skus'] = skus

        hrefs = response.css(".swatches.color > li[class='selectable'] > a::attr('href')")
        colour_priority = len(hrefs)

        if not hrefs:
            yield response.meta['product']

        for href in hrefs:
            request = scrapy.Request(href.extract(), callback=self.parse_colours,
                                     priority=colour_priority)
            request.meta['product'] = response.meta['product']
            colour_priority -= 1
            request.meta['request'] = colour_priority
            yield request

    def parse_colours(self, response):
        variants = self.variant_sizes_and_availability(response)
        skus = self.get_skus(response,  variants)
        response.meta['product']['skus'].update(skus)

        if response.meta['request'] == 0:
            return response.meta['product']

    def product_start_link(self, response):
        return response.css('.variation-select option::attr(value)').extract_first()

    def processed_products(self, product_id):
        if product_id in self.processed_pids:
            return True
        else:
            self.processed_pids.add(product_id)
            return False

    def product_id(self, response):
        return response.css('span::attr(data-masterid)').extract_first()

    def product_brand(self, response):
        return response.css('#productData::attr(data-brand)').extract_first()

    def product_category(self, response):
        return response.css('h1.product-name::text').extract()

    def product_description_and_care(self, response):
        parent_class = response.css('div#tab1::text').extract_first().strip()
        care = r"De stof(.*)\."
        return re.split(care, parent_class)

    def image_urls(self, response):
        image_urls = response.css('.productthumbnail::attr(src)').extract()
        return [url.replace('small', 'large') for url in image_urls]

    def gender(self, response):
        return response.css('.breadcrumb-element::text').extract_first()

    def construct_sku_id(self, product_id, size, colour):
        return "{0}_{1}_{2}".format(product_id, colour, size)

    def variant_sizes_and_availability(self, response):
        sizes = response.css('.variation-select option::text').extract()
        variants = []

        for i in range(1, len(sizes)):
            availability = True if 'uitverkocht' in sizes[i] else False
            variants.append((sizes[i].strip(), availability))
        return variants

    def construct_sku(self, response):
        sku = {}
        sku['currency'] = response.css('.price::text').extract_first()[:3]
        sku['colour'] = response.css('.selected-value::text').extract_first()

        parent_class = response.css('.product-price')

        if parent_class.css('.price-standard::text').extract():
            sku['previous_prices'] = parent_class.css('.price-standard::text').extract()

        sku['price'] = parent_class.css('.price-sales::text').extract()
        return sku

    def get_skus(self, response, variants):
        skus = {}
        sku = self.construct_sku(response)
        for size, available in variants:
            sku['out_of_stock'] = available
            sku['size'] = size
            product_id = response.css('span::attr(data-masterid)').extract_first()
            skus[self.construct_sku_id(product_id, size, sku['colour'])] = sku

        return skus