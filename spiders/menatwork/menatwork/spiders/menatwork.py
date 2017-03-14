import re
from scrapy.spiders import CrawlSpider
from scrapy import Request
from menatwork.items import MenatworkItem


class MenatworkSpider(CrawlSpider):
    name = 'menatwork'
    allowed_domains = ['menatwork.nl']
    seen_ids = set()

    def start_requests(self):
        start_urls = ['http://menatwork.nl/nl_NL/dames/',
                      'http://menatwork.nl/nl_NL/heren/']

        for url in start_urls:
            yield Request(url, callback=self.total_products_url)

    def total_products_url(self, response):
        total_items = self.total_items(response).replace('.', '').strip()
        start_url = response.url + '?sz=' + total_items
        yield Request(start_url, callback=self.parse_products)

    def parse_products(self, response):
        urls = response.css('.thumb-link::attr(href)').extract()
        for url in urls:
            yield Request(url, callback=self.parse_product)

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
        product['name'] = self.product_name(response)
        product['retailer_sku'] = self.product_id(response)

        product_url = self.product_url(response)

        yield Request(product_url, callback=self.parse_variants,
                      meta={'product': product})

    def parse_variants(self, response):
        available_sizes = self.variant_sizes_and_availability(response)
        skus = self.skus(response, available_sizes)
        response.meta['product']['skus'] = skus

        variants = response.css(".swatches.color > li[class='selectable'] "
                                "> a::attr('href')")
        requests = []
        if not variants:
            yield response.meta['product']
            return

        for variant in variants:
            request = Request(variant.extract(), callback=self.parse_colours)
            request.meta['product'] = response.meta['product']
            requests.append(request)

        yield self.variant_request(requests)

    def parse_colours(self, response):
        variants = self.variant_sizes_and_availability(response)
        skus = self.skus(response,  variants)
        response.meta['product']['skus'].update(skus)
        response.meta['product']['image_urls'].append(self.image_urls(response))
        requests = response.meta['pending_requests']

        if requests:
            yield self.variant_request(requests)
        else:
            yield response.meta['product']

    def variant_request(self, requests):
        request = requests.pop()
        request.meta['pending_requests'] = requests
        return request

    def total_items(self, response):
        return response.css('.results-hits-amount::text').extract_first()

    def product_url(self, response):
        url = response.css('.variation-select option::attr(value)').extract_first()
        return response.urljoin(url)

    def processed_products(self, product_id):
        if product_id in self.seen_ids:
            return True
        self.seen_ids.add(product_id)
        return False

    def product_id(self, response):
        return response.css('span::attr(data-masterid)').extract_first()

    def product_brand(self, response):
        return response.css('#productData::attr(data-brand)').extract_first()

    def product_name(self, response):
        return response.css('h1.product-name::text').extract()

    def product_category(self, response):
        return response.css('.breadcrumb-element:nth-child(4)::text').extract()

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

    def variant_sizes_and_availability(self, response):
        sizes = response.css('.variation-select option::text').extract()
        sizes = sizes[1:] if sizes[0] == 'Kies Maat' else sizes

        return [(size.strip(), 'uitverkocht' in size) for size in sizes]

    def common_sku(self, response):
        sku = {}
        sku['currency'] = response.css('.price::text').re(r'[A-Z]*')[0]
        sku['colour'] = response.css('.selected-value::text').extract_first()

        parent_class = response.css('.product-price')

        if parent_class.css('.price-standard::text').extract():
            sku['previous_prices'] = parent_class.css('.price-standard::text').extract()

        sku['price'] = parent_class.css('.price-sales::text').extract_first()
        return sku

    def skus(self, response, variants):
        skus = {}
        product_id = self.product_id(response)

        for size, availability in variants:
            sku = self.common_sku(response)
            sku['out_of_stock'] = availability
            sku['size'] = size
            sku_id = "{0}_{1}_{2}".format(product_id, sku['colour'], size)
            skus[sku_id] = sku

        return skus
