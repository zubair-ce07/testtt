import re
from w3lib.url import add_or_replace_parameter
from w3lib.url import url_query_cleaner
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from menatwork.items import MenatworkItem


class MenatworkSpider(CrawlSpider):
    name = 'menatwork'
    allowed_domains = ['menatwork.nl']
    start_urls = ['http://menatwork.nl/']

    rules = (

        Rule(LinkExtractor(restrict_css=('.search-result-content',)),
             callback='parse_product', process_links='process_links'),

        Rule(LinkExtractor(allow=(r'/nl_NL/dames/$', r'/nl_NL/heren/$'),
                           restrict_css='.teaser__block--half'),
             callback='parse_pagination'),

    )

    seen_ids = set()

    def process_links(self, links):
        for link in links:
            link.url = url_query_cleaner(link.url, ['.html'])

        return links

    def parse_pagination(self, response):
        items = response.css('.results-hits-amount::text').extract_first()
        total_items = int(items.replace('.', '').strip())

        for i in range(24, total_items, 12):
            next_url = add_or_replace_parameter(response.url, "sz", i)
            yield Request(response.urljoin(next_url))

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
        product['retailer_sku'] = product_id

        response.meta['product'] = product
        return self.variants(response)

    def variants(self, response):
        available_sizes = self.variant_sizes_and_availability(response)
        skus = self.skus(response, available_sizes)
        response.meta['product']['skus'] = skus

        variants = response.css(".swatches.color > li[class='selectable'] "
                                "> a::attr('href')")
        requests = []

        for variant in variants:
            request = Request(variant.extract(), callback=self.parse_colours)
            request.meta['product'] = response.meta['product']
            requests.append(request)

        return self.variant_request(requests, response)

    def parse_colours(self, response):
        variants = self.variant_sizes_and_availability(response)
        skus = self.skus(response,  variants)
        response.meta['product']['skus'].update(skus)
        response.meta['product']['image_urls'] += self.image_urls(response)
        requests = response.meta['pending_requests']

        return self.variant_request(requests, response)

    def variant_request(self, requests, response):
        if requests:
            request = requests.pop()
            request.meta['pending_requests'] = requests
            return request
        return response.meta['product']

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
        return response.css('h1.product-name::text').extract_first()

    def product_category(self, response):
        return response.css('.breadcrumb-element:nth-child(4)::text').extract()

    def product_description_and_care(self, response):
        description_and_care = response.css('div#tab1::text').extract_first().strip()
        care = r"De stof(.*)\."

        description = [re.split(care, description_and_care)[0]]
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
        sku['colour'] = response.css('.selected-value::text').extract_first()

        price = response.css('.price::text')
        sku['currency'] = price.re(r'[A-Z]*')[0]
        sku['price'] = float(price.re(r'\d+\.*\d+')[0])

        parent_class = response.css('.product-content')
        previous_prices = parent_class.css('.price-standard::text')
        if previous_prices.extract():
            sku['previous_prices'] = [float(price.re(r'\d+\.*\d+')[0]) for price
                                      in previous_prices]

        return sku

    def skus(self, response, variants):
        skus = {}
        common_sku = self.common_sku(response)

        for size, availability in variants:
            sku = common_sku.copy()
            sku['out_of_stock'] = availability
            sku['size'] = size
            sku_id = "{0}_{1}".format(sku['colour'], size)
            skus[sku_id] = sku

        return skus
