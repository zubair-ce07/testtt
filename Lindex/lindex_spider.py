import re
import xml.etree.ElementTree as Etree

from scrapy import FormRequest
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'lindex-uk'
    market = 'UK'
    allowed_domains = ['lindex.com']
    start_urls = ['https://www.lindex.com/uk/']


class LindexParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    price_css = '#ProductPage .price ::text'

    category_re = re.compile('(\s*›)')
    size_re = re.compile('([0-9a-zA-Z]+)\s*\(.*\)')

    xml_tag_prefix = '{http://lindex.com/WebServices}'
    image_url_p = 'https://lindex-static.akamaized.net'
    product_data_url = 'https://www.lindex.com/WebServices/ProductService.asmx/GetProductData'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = {}
        garment['image_urls'] = []
        garment['gender'] = self.product_gender(response)

        garment['meta'] = {
            'requests_queue': self.colour_requests(response),
            'pricing': self.product_pricing_common_new(response)
        }

        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        requests = []

        form_data = {
            'primaryImageType': '1',
            'isMainProductCard': 'true',
            'nodeId': self.product_page_id(response),
            'productIdentifier': self.product_id(response)
        }

        colour_ids = self.product_colour_ids(response)

        for colour_id in colour_ids:
            form_data['colorId'] = colour_id

            requests += [FormRequest(
                url=self.product_data_url,
                formdata=form_data,
                callback=self.parse_colour_data
            )]

        return requests

    def parse_colour_data(self, response):
        garment = response.meta['garment']

        xml_response = Etree.fromstring(response.text)

        garment['image_urls'] += self.image_urls(xml_response)
        garment['skus'].update(
            self.skus(xml_response, garment['meta']['pricing']))

        return self.next_request_or_garment(garment)

    def skus(self, xml_response, pricing):
        skus = {}

        sizes = self.colour_sizes(xml_response)
        colour = self.product_colour(xml_response)
        is_sold_out = self.color_stock_status(xml_response)

        for size in sizes:
            sku = {
                'size': size if size != '0' else self.one_size,
                'colour': colour
            }

            if is_sold_out:
                sku['out_of_stock'] = True

            sku.update(pricing)
            skus[colour+'_'+size] = sku

        return skus

    def color_stock_status(self, xml_response):
        xpath = '{0}IsSoldOut'.format(self.xml_tag_prefix)
        colour_stock = xml_response.findall(xpath)

        return 'true' in colour_stock[0].text

    def image_urls(self, xml_response):
        xpath = '{0}Images//{0}Image/{0}XLarge'.format(self.xml_tag_prefix)

        image_urls = xml_response.findall(xpath)

        return [self.image_url_p + img.text
                for img in image_urls]

    def product_colour(self, xml_response):
        xpath = '{0}Color'.format(self.xml_tag_prefix)
        colour = xml_response.findall(xpath)

        return colour[0].text

    def colour_sizes(self, xml_response):
        xpath = '{0}SizeInfo//{0}SizeInfo/{0}Text'.format(self.xml_tag_prefix)

        sizes_xml = xml_response.findall(xpath)
        nested_sizes = [self.size_re.findall(size.text)
                            for size in sizes_xml]

        return sum(nested_sizes, [])

    def product_colour_ids(self, response):
        css = '.product .colors ::attr(data-colorid)'

        return clean(response.css(css))

    def product_page_id(self, response):
        css = ' ::attr(data-page-id)'

        return clean(response.css(css))[0]

    def product_brand(self, response):
        css = '#ProductPage ' \
              '::attr(data-product-brand)'

        return clean(response.css(css))[0]

    def product_gender(self, response):
        gender = 'unisex-kids' if 'kids' in response.url else 'women'

        return gender

    def product_id(self, response):
        css = '.product_id::text'

        return clean(response.css(css))[0]

    def product_category(self, response):
        css = '#breadcrumbs ::text'
        category = clean(response.css(css))[1:]

        category = [self.category_re.sub('', cat)
                    for cat in category]

        return clean(category)

    def product_name(self, response):
        css = '.name::text'

        return clean(response.css(css))[0]

    def raw_description(self, response):
        css = '.description ::text'

        return clean(response.css(css))

    def product_description(self, response):
        return [rd for rd in self.raw_description(response)
                if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        css = '.more_info ::text'
        care = clean(response.css(css))

        care += [rd for rd in self.raw_description(response)
                 if self.care_criteria_simplified(rd)]

        return care


class LindexCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = LindexParseSpider()

    listing_css = '.mainMenu'

    pagination_css = '.aside.nav'

    product_css = '.gridPage .img_wrapper .productCardLink'

    page_api_url = 'https://www.lindex.com/uk/SiteV3/Category/GetProductGridPage'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=pagination_css), callback='parse_pagination'),
    )

    def parse_pagination(self, response):
        return self.paging_requests(response)

    def paging_requests(self, response):
        requests = []
        pages = self.total_pages(response)
        category_id = self.category_id(response)

        form_data = {'nodeId': category_id}

        for page in range(1, pages):
            form_data['pageIndex'] = str(page)

            requests += [FormRequest(url=self.page_api_url,
                                     formdata=form_data)]
        return requests

    def total_pages(self, response):
        css = ' ::attr(data-page-count)'

        return int(clean(response.css(css))[0])

    def category_id(self, response):
        css = ' ::attr(data-page-id)'

        return clean(response.css(css))[0]

