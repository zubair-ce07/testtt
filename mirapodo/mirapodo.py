import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean
from titlecase import titlecase
import json


class Mixin(object):
    lang = 'de'
    market = 'DE'
    retailer = 'mirapodo-de'
    allowed_domains = ['mirapodo.de']
    start_urls = ['http://www.mirapodo.de/']


class MirapodoParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    PRICE_X = '//div[@id="price"]//span[1]//text() | //div[@id="price"]//s//text()'

    GENDER_MAP = [
        ("girl", "girls"),
        ("mädchen", "girls"),
        ("madchen", "girls"),
        ("maedchen", "girls"),
        ("boy", "boys"),
        ("jungen", "boys"),
        ("damen", "women"),
        ("herren", "men"),
        ("kinder", "unisex-kids"),
    ]

    unwanted_description = [
        'produktdetails',
        'weiterlesen',
        '{'
    ]

    CARE_COLUMNS = [
        'Obermaterial:', 'Futter:', 'Decksohle:',
        'Laufsohle:'
    ]

    def parse(self, response):
        pid = self.product_id(response.url)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response, response)
        garment['merch_info'] = self.merch_info(response)
        garment['gender'] = self.product_gender(garment)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['image_urls'] += self.image_urls(response)

        return self.next_request_or_garment(garment)

    def skus(self, response):
        skus = {}
        sku_common = self.product_pricing_common(response)
        sku_common['colour'] = colour = clean(response.css('.product-color span::text'))[0]

        sizes_s = response.css('.productSizes li')
        for s_s in sizes_s:
            sku = sku_common.copy()
            size = clean(s_s.css('strong::text'))[0]
            sku['size'] = size = self.one_size if size == 'UNI' else size

            if s_s.css(".notavailable"):
                sku['out_of_stock'] = True
            skus[colour + '_' + size] = sku

        return skus

    def colour_requests(self, response):
        css = '.color-selection li:not(.selected) a::attr(href)'
        colour_links = clean(response.css(css))

        return [Request(link, callback=self.parse_colour) for link in colour_links]

    def product_id(self, url):
        return re.findall('-sku(\d+)\.html', url)[0]

    def image_urls(self, response):
        data = json.loads(clean(response.css('#productData::text'))[0])
        return [image['url-xxl'] for image in data['product'].get('images')]

    def product_brand(self, response):
        return titlecase(re.findall('_brand":\s+"(.*?)",', self.raw_data(response))[0])

    def product_name(self, response):
        name = titlecase(re.findall('_name":\s+"(.*?)",', self.raw_data(response))[0])
        return re.sub('^{0} '.format(self.product_brand(response)), '', name).strip()

    def raw_data(self, response):
        return clean(response.css('body .tag_track::text'))[0]

    def product_category(self, response):
        css = '#breadcrumb a::text, #breadcrumb span::text'
        return clean(response.css(css)[1:])

    def product_description(self, response):
        raw_desc = self.raw_description(response)
        return [d for d in raw_desc if self.description_criteria(d)]

    def description_criteria(self, desc):
        return not (self.care_criteria(desc) or any(dw in desc.lower() for dw in self.unwanted_description))

    def product_care(self, response):
        raw_desc = self.raw_description(response)
        return [d for d in raw_desc if self.care_criteria(d)]

    def care_criteria(self, care):
        return super(MirapodoParseSpider, self).care_criteria(care) or any(cc in care for cc in self.CARE_COLUMNS)

    def raw_description(self, response):
        desc = re.findall('>(.*?)<', clean(response.css('#details_success, .details')[0]))
        return [re.sub('^-', '', d).strip() for d in desc if d.strip()]

    def merch_info(self, response):
        css = '.productdetailFlags span::text'
        return clean(response.css(css))

    def product_gender(self, garment):
        gender_soup = " ".join(garment['category'] + [t[1] for t in garment['trail'] or []]).lower()

        for gender_str, gender in self.GENDER_MAP:
            if gender_str in gender_soup:
                return gender

        return "unisex-adults"


class MirapodoCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = MirapodoParseSpider()

    allow_r = [
        '/damen/',
        '/herren/',
        '/kinder/',
        '/taschen/'
    ]

    listings_css = [
        '.categories a',
        '.pagination .next'
    ]

    products_css = [
        '.productTile a'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=listings_css, allow=allow_r), callback='parse'),
    )
