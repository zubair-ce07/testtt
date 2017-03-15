import re
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from menatwork.items import MenatworkItem


class MenatworkSpider(CrawlSpider):
    name = 'menatwork'
    allowed_domains = ['menatwork.nl']
    start_urls = ['http://menatwork.nl/']

    rules = (

        Rule(LinkExtractor(restrict_css=('.search-result-content',)),
             callback='parse_product', follow=True),

        Rule(LinkExtractor(allow=(r'/nl_NL/dames/$', r'/nl_NL/heren/$')),
             callback='parse_all_products', follow=True),

    )

    seen_ids = set()

    def parse_all_products(self, response):
        xpath = '//link[@rel="next"]/@href'
        base_url = response.xpath(xpath).extract_first()
        items = response.css('.results-hits-amount::text').extract_first()
        total_items = int(items.replace('.', '').strip()) if items else 0

        for i in range(24, total_items, 12):
            previous_query = urlparse(base_url).query
            next_query = "{0}{1}".format('sz=', i)
            next_url = base_url.replace(previous_query, next_query)
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
        else:
            return response.meta['product']

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
        price = response.css('.price::text')
        sku['currency'] = price.re(r'[A-Z]*')[0]
        sku['price'] = float(price.re(r'\d+\.*\d+')[0])

        sku['colour'] = response.css('.selected-value::text').extract_first()

        parent_class = response.css('.product-price')

        if parent_class.css('.price-standard::text').extract():
            sku['previous_prices'] = parent_class.css('.price-standard::text').extract()

        return sku

    def skus(self, response, variants):
        skus = {}
        product_id = self.product_id(response)
        common_sku = self.common_sku(response)

        for size, availability in variants:
            sku = common_sku.copy()
            sku['out_of_stock'] = availability
            sku['size'] = size
            sku_id = "{0}_{1}_{2}".format(product_id, sku['colour'], size)
            skus[sku_id] = sku

        return skus
