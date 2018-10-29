import json

from scrapy import Spider
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import Item
from ..utilities import convert_price_to_integer


class SoftsurroundingsParseSpider(Spider):
    name = 'softsurroundings-parse'
    product_url_t = 'https://www.softsurroundings.com/p'

    allowed_domains = ['softsurroundings.com']

    def parse(self, response):
        item = Item()

        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['name'] = self.extract_name(response)
        item['care'] = self.extract_care(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['description'] = self.extract_description(response)
        item['category'] = self.extract_category(response)
        item['url'] = response.url

        item['skus'] = {}
        item['meta'] = {}

        item['meta']['requests'] = self.create_size_type_requests(response)
        item['meta']['requests'] += self.create_colour_requests(response)

        yield self.generate_next_request_or_item(item)

    def parse_size_type(self, response):
        item = response.meta['item']
        item['meta']['requests'] += self.create_colour_requests(response)
        yield self.generate_next_request_or_item(item)

    def parse_colour(self, response):
        item = response.meta['item']
        item['meta']['requests'] += self.create_size_requests(response)
        yield self.generate_next_request_or_item(item)

    def parse_size(self, response):
        item = response.meta['item']
        item['skus'].update(self.extract_skus(response))
        yield self.generate_next_request_or_item(item)

    def generate_next_request_or_item(self, item):
        if item['meta'].get('requests'):
            request = item['meta']['requests'].pop()
            request.meta['item'] = item
            return request
        
        del item['meta']
        return item

    def create_size_type_requests(self, response):
        size_types_css = '#sizecat > a:not(.sel)::attr(id)'

        raw_size_types = response.css(size_types_css).extract()

        if not raw_size_types:
            return []

        requests = []
        size_type_codes = [size_type.split('_')[1]
                           for size_type in raw_size_types]

        for size_type_code in size_type_codes:
            url = response.urljoin(f'/p/{size_type_code.lower()}/')
            requests.append(Request(url, callback=self.parse_size_type))
        return requests

    def create_colour_requests(self, response):
        size_type_code = response.url.split('/')[-2]

        colours_css = '#color img::attr(data-value)'
        colour_codes = [code for code in response.css(colours_css).extract() if code]
        if not colour_codes:
            return self.create_size_requests(response)

        requests = []
        for colour_code in colour_codes:
            url = response.urljoin(f'/p/{size_type_code.lower()}/{colour_code}/')
            requests.append(Request(url, callback=self.parse_colour))
        return requests

    def create_size_requests(self, response):
        size_type_css = 'input[name*="sizecat"]::attr(value)'
        size_type_code = response.css(size_type_css).extract_first()

        colour_css = 'input[name*="specOne"]::attr(value)'
        colour_code = response.css(colour_css).extract_first()

        sizes_css = 'div[id="size"] > a::attr(id)'
        size_selected_css = 'input[name*="specTwo"]::attr(value)'

        raw_sizes = response.css(sizes_css).extract()
        size_codes = ([size.split('_')[1] for size in raw_sizes] or
                      response.css(size_selected_css).extract())

        requests = []
        for size_code in size_codes:
            url = response.urljoin(f'/p/{size_type_code.lower()}/{colour_code}{size_code}/')
            requests.append(Request(url, callback=self.parse_size))
        return requests

    def extract_retailer_sku(self, response):
        retailer_sku_css = 'input[name="uniqid"]::attr(value)'
        return response.css(retailer_sku_css).extract_first()

    def extract_name(self, response):
        name_css = 'span[itemprop="name"]::text'
        return response.css(name_css).extract_first()

    def extract_care(self, response):
        care_css = 'div.tabContent > span::text'
        return response.css(care_css).extract()
    
    def extract_image_urls(self, response):
        image_urls_css = 'div.dtlAltThms img::attr(src)'
        return response.css(image_urls_css).extract()

    def extract_description(self, response):
        description_css = 'div.productInfo::text, p.p1::text'
        return response.css(description_css).extract()

    def extract_category(self, response):
        category_css = 'div.pagingBreadCrumb *::text'
        return [cat for cat in response.css(category_css).extract() if '/' not in cat]

    def extract_price(self, response):
        price_css = 'span[itemprop="price"]::text'
        price = response.css(price_css).extract_first()
        return convert_price_to_integer(price)

    def extract_currency(self, response):
        currency_css = 'span[itemprop="priceCurrency"]::attr(content)'
        return response.css(currency_css).extract_first()

    def extract_previous_price(self, response):
        previous_price_css = 'div.ctntPrice::text'
        previous_price = response.css(previous_price_css).extract_first()
        if previous_price:
            previous_price = previous_price.split(' ')[1].replace(';', '')[1:]
            return convert_price_to_integer(previous_price)

    def extract_skus(self, response):
        size_css = '#size b.basesize::text'
        size = response.css(size_css).extract_first()

        colour_css = '#color b.basesize::text'
        colour = response.css(colour_css).extract_first()

        size_type_css = '#sizecat > a.sel::text'
        size_type = response.css(size_type_css).extract_first()

        availability_css = 'p.sizetbs.stockStatus b.basesize::text'
        availability = response.css(availability_css).extract_first()

        sku = {}
        sku['currency'] = self.extract_currency(response)
        sku['price'] = self.extract_price(response)
        sku['colour'] = colour
        sku['size'] = '/'.join([s for s in [size_type, size] if s])

        if not availability:
            sku['out_of_stock'] = True

        previous_price = self.extract_previous_price(response)
        if previous_price:
            sku['previous_price'] = previous_price

        sku_id = f'{colour}_{size}'
        return {sku_id: sku}


class SoftsurroundingsCrawlSpider(CrawlSpider):
    name = 'softsurroundings-crawl'

    allowed_domains = ['softsurroundings.com']
    start_urls = ['https://www.softsurroundings.com/']

    listings_x = ['//ul[contains(@class, "categories")]']
    products_x = ['//div[contains(@class, "thmImgWrap")]']
    deny = ['gift-card']
    
    custom_settings = {
        'DOWNLOAD_DELAY' : '1'
    }
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_x, deny=deny), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_xpaths=products_x, deny=deny), callback='parse_product'),
    )
    
    product_parser = SoftsurroundingsParseSpider()

    def parse_pagination(self, response):
        last_page_no_css = 'form.thumbscroll:last-of-type > input[name="page"]::attr(value)'
        last_page_no = response.css(last_page_no_css).extract_first()

        url = f'{response.url}page-{last_page_no}/' if last_page_no else response.url
        yield Request(url, callback=self.parse, dont_filter=True)

    def parse_product(self, response):
        yield from self.product_parser.parse(response)
