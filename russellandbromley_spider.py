import json
import re

from parsel import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from skuscraper.spiders.base import BaseCrawlSpider, BaseParseSpider, Gender, clean

from w3lib.url import add_or_replace_parameter


class Mixin:
    retailer = 'russellandbromley'


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    allowed_domains = ['russellandbromley.co.uk']
    start_urls = ['http://www.russellandbromley.co.uk/']


class RussellAndBromleyParseSpider(BaseParseSpider):
    care_css = '.detailsWrapper ::text'
    raw_description_css = '.invtdesc1 .scrollWrap ::text'
    price_css = '.oneProduct .priceField ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        item = response.meta['garment']
        item['skus'].update(self.skus(response))
        item['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(item)

    def product_id(self, response):
        css = '#tag-invtref::text'
        return clean(response.css(css).extract()[0][:4])

    def product_name(self, response):
        css = '#tag-invtname::text'
        return clean(response.css(css).extract()[0])

    def product_brand(self, response):
        css = '.logoBox.grid_5 a::attr(title)'
        return clean(response.css(css).extract()[0])

    def product_category(self, response):
        css = '.crumbtrail a::text'
        return clean(response.css(css).extract()[1:])

    def product_gender(self, response):
        css = '.crumbtrail a::text, .scrollWrap ::text'
        soup = ' '.join(clean(response.css(css).extract()))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def image_urls(self, response):
        css = '#productdetail-altview ~ script:contains(StoreImageSwaps)'
        raw_urls = clean(response.css(css).extract()[0])
        raw_urls = re.findall(f'imgL: \[(.*?)\]', raw_urls)[0].split(',')
        return [url.replace('"', '') for url in raw_urls if url != '""']

    def attribute_from_text(self, text, attr, is_string=True):
        if is_string:
            return re.findall(f'{attr}":"(.*?)"', text)[0]

        return int(re.findall(f'{attr}":(.*?),', text)[0])

    def sku_colour(self, response):
        x = "//*[contains(@name, 'oitemxoixtcolour')]/@value"
        return response.xpath(x).extract()[0]

    def skus(self, response):
        css = 'script:contains(StoreJSON)'
        raw_skus = response.css(css).re('{.*}')
        skus = {}
        common_sku = self.product_pricing_common(response)
        common_sku['colour'] = self.sku_colour(response)

        for raw_sku in raw_skus:
            sku = common_sku.copy()
            sku['size'] = self.attribute_from_text(raw_sku, 'att1')
            sku_id = self.attribute_from_text(raw_sku, 'atrsku')

            if not self.attribute_from_text(raw_sku, 'atronhand', False):
                sku['out_of_stock'] = True

            skus[sku_id] = sku

        return skus

    def colour_requests(self, response):
        css = '#otherColoursMaterials a::attr(href)'
        urls = response.css(css).extract()
        requests = []

        for url in set(urls):
            requests.append(response.follow(url, callback=self.parse_colour))

        return requests


class RussellAndBromleyCrawlSpider(BaseCrawlSpider):
    listing_css = [
        '#mm_ul',
    ]

    sub_listing_css = [
        '.categoryNavigation',
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=sub_listing_css), callback='parse_listing'),
    ]

    listing__request_url_t = 'http://fsm.attraqt.com/zones-js.aspx?' \
                             'siteId=ba6279ce-57d8-4069-8651-04459b92bceb&zone0=category'

    def parse_listing(self, response):
        return self.listing_request(response)

    def parse_products(self, response):
        return self.product_requests(response)

    def product_requests(self, response):
        raw_urls = json.loads(re.findall('{.*}', response.text)[1])
        raw_urls = Selector(raw_urls['html'])
        urls = raw_urls.css('.image a::attr(href)').extract()
        response.meta['trail'] = self.add_trail(response)

        requests = []

        for url in urls:
            request = response.follow(f'http://www.russellandbromley.co.uk{url}',
                                      callback=self.parse_item)
            request.meta['trail'] = self.add_trail(response)
            requests.append(request)

        url = response.meta.get('request_url')

        if not url:
            return requests

        css = ".pagnNumbers a[rel='next']::attr(href)"
        page_url = raw_urls.css(css).extract_first()

        if not page_url:
            return requests

        page_url = f'http://www.russellandbromley.co.uk{page_url}'
        url = add_or_replace_parameter(url, 'pageurl', response.url)
        url = add_or_replace_parameter(url, 'pageurl', page_url)
        requests.append(response.follow(url, callback=self.parse_products, dont_filter=True))

        return requests

    def listing_request(self, response):
        url = add_or_replace_parameter(self.listing__request_url_t,
                                       'config_categorytree', self.exract_category(response))
        url = add_or_replace_parameter(url, 'pageurl', response.url)
        url = add_or_replace_parameter(url, 'mergehash', 'true')

        category_values = self.exract_category(response)
        url = add_or_replace_parameter(url, 'config_categorytree', category_values[0])
        url = add_or_replace_parameter(url, 'config_parentcategorytree', category_values[1])
        url = add_or_replace_parameter(url, 'config_category', category_values[2])

        meta = {'request_url': url}
        return response.follow(url, callback=self.parse_products, meta=meta, dont_filter=True)

    def exract_category(self, response):
        css = 'script:contains(config)'
        raw_category = response.css(css)
        return raw_category.re(r'"categorytree","(.*?)"')[0], \
               raw_category.re(r'"parentcategorytree","(.*?)"')[0], \
               raw_category.re(r'"category","(.*?)"')[0]


class RussellAndBromleyUKParseSpider(MixinUK, RussellAndBromleyParseSpider):
    name = MixinUK.retailer + '-parse'


class RussellAndBromleyUKCrawlSpider(MixinUK, RussellAndBromleyCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = RussellAndBromleyUKParseSpider()
