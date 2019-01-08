import json

from scrapy import Spider, Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from item_structure import Item
from helpers import extract_price_details, item_or_request


class ProductParser(Spider):
    def __init__(self):
        self.seen_ids = set()

    def parse(self, response):
        item = Item()
        retailer_sku = self.extract_id(response)

        if not self.is_new_item(retailer_sku):
            return

        item['name'] = self.extract_name(response)
        item['gender'] = self.extract_gender()
        item['retailer_sku'] = retailer_sku
        item['care'] = self.extract_care(response)
        item['url'] = response.url
        item['spider_name'] = 'lanebryant'
        item['market'] = self.extract_market()
        item['retailer'] = self.extract_retailer()
        item['brand'] = self.extract_brand()
        item['category'] = self.extract_category(response)
        item['description'] = self.extract_description(response)
        item['trail'] = response.meta.get('trail', [])
        item['skus'] = self.extract_skus(response)
        item['meta'] = {'requests': self.extract_images_requests(response)}
        item['image_urls'] = self.extract_image_urls(response)

        return item_or_request(item)

    def parse_images(self, response):
        item = response.meta.get('item', {})
        item['image_urls'] += self.extract_image_urls(response)
        return item_or_request(item)

    def extract_images_requests(self, response):
        pattern = 'all_available_colors":.*?values":(.*?),"option_key'
        image_dataset = response.xpath('//script[@id="pdpInitialData"]/text()').re_first(pattern)
        image_requests = []

        if image_dataset:
            for image in json.loads(image_dataset):
                url = f"{response.urljoin(image['sku_image'])}_ms?req=set,json&id={image['id']}"
                image_requests.append(Request(url=url, callback=self.parse_images))

        return image_requests

    def is_new_item(self, retailer_sku):
        if retailer_sku and retailer_sku not in self.seen_ids:
            self.seen_ids.add(retailer_sku)
            return True

        return False

    def extract_id(self, response):
        return response.css('[id=pdpProductID]::attr(value)').extract_first()

    def extract_name(self, response):
        return response.css('.mar-product-title::text').extract_first()

    def extract_care(self, response):
        css = '.mar-product-additional-info--tab-item ul:nth-child(3) li::text'
        raw_care = response.css(css).extract()
        return [care.strip() for care in raw_care if care.strip()]

    def extract_category(self, response):
        raw_category = response.xpath("//script/text()").re('category": "(.*?.)"')
        return [category.strip() for category in raw_category]

    def extract_description(self, response):
        description = response.css('.mar-product-additional-info--tab-item [id=tab1] p::text').extract()
        if not description:
            return description
        return [des.strip() for des in description[0].split('.') if des.strip()]

    def extract_skus(self, response):
        skus = {}
        in_stock_items = self.extract_in_stock_items(response)

        for raw_sku in self.extract_raw_skus(response):
            sku = extract_price_details(self.extract_price(raw_sku, response))
            sku['colour'] = self.extract_colour(raw_sku['color'], response)
            sku['size'] = self.extract_size_value(raw_sku['size'], response)

            if raw_sku['size'] not in in_stock_items:
                sku['out_of_stock'] = True

            skus[f"{sku['colour']}_{sku['size']}"] = sku

        return skus

    def extract_market(self):
        return 'US'

    def extract_image_urls(self, response):
        raw_image_urls = response.xpath('//text()').re('item":(.*?])')
        if raw_image_urls:
            parent_url = 'https://lanebryant.scene7.com/is/image'
            raw_image_urls = [f"{parent_url}/{image['s']['n']}" for image in json.loads(raw_image_urls[0])]

        return raw_image_urls

    def extract_size_value(self, size_id, response):
        pattern = f'{{"id":"{size_id}".*?"value":"(.*?)"'
        return response.xpath('//script[@id="pdpInitialData"]/text()').re_first(pattern)

    def extract_retailer(self):
        return 'lanebryant'

    def extract_gender(self):
        return 'Women'

    def extract_currency(self, response):
        return response.xpath('//script/text()').re_first('"currency".*?"(.*?)"')

    def extract_brand(self):
        return 'Lane Bryant'

    def extract_raw_skus(self, response):
        xpath = '//script[@id="pdpInitialData"]/text()'
        pattern = '"skus":(\[.*?\]),"badge"'
        return json.loads(response.xpath(xpath).re_first(pattern))

    def extract_colour(self, colour_id, response):
        pattern = f'{{"id":"{colour_id}".*?"name":"(.*?)"'
        return response.xpath('//script[@id="pdpInitialData"]/text()').re_first(pattern)

    def extract_price(self, raw_sku, response):
        prices = []
        prices.append(raw_sku['prices']['sale_price'])
        prices.append(raw_sku['prices']['list_price'])
        prices.append(self.extract_currency(response))
        return prices

    def extract_in_stock_items(self, response):
        pattern = 'all_available_sizes":.*?"values":(.*),"option'
        in_stock_items = response.xpath('//script[@id="pdpInitialData"]/text()').re_first(pattern)
        return [item['id'] for item in json.loads(in_stock_items)]


class LaneBryantSpider(CrawlSpider):
    name = 'lanebryant-crawl-spider'
    allowed_domains = ['www.lanebryant.com','lanebryant.scene7.com']
    start_urls = ['http://www.lanebryant.com/']
    product_parser = ProductParser()

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36'
    }

    product_css = ['.asc-brand-header','.mar-plp-header-section']
    listing_css = ['.mar-main-content']
    rules = [
        Rule(LinkExtractor(restrict_css=product_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_item')
    ]

    def parse(self, response):
        title = self.extract_title(response)
        trail = response.meta.get('trail', [])
        trail = trail + [[title, response.url]]

        for request in super().parse(response):
            request.meta['trail'] = trail.copy()
            yield request

    def parse_item(self, response):
        return self.product_parser.parse(response)

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        return title.split('|')[0] or None
