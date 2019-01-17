import json

from scrapy import Spider, Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from item_structure import Item
from helpers import extract_price_details


class ProductParser(Spider):
    def __init__(self):
        self.seen_ids = set()

    def parse(self, response):
        item = Item()
        retailer_sku = self.extract_product_id(response)

        if not self.is_new_item(retailer_sku):
            return

        item['retailer_sku'] = retailer_sku
        item['name'] = self.extract_name(response)
        item['gender'] = self.extract_gender()
        item['spider_name'] = 'savagex'
        item['brand'] = self.extract_brand()
        item['url'] = response.url
        item['trail'] = response.meta.get('trail', [])
        item['retailer'] = self.extract_retailer()
        item['market'] = self.extract_market()
        item['description'] = self.extract_description(response)
        item['care'] = self.extract_care(response)
        item['category'] = self.extract_categories(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['skus'] = self.extract_skus(response)

        return item

    def is_new_item(self, product):
        if product and product not in self.seen_ids:
            self.seen_ids.add(product)
            return True

        return False

    def extract_product_id(self, response):
        xpath = "//script[contains(.,'product')]/text()"
        return response.xpath(xpath).re_first('"query".*productId":"(.*?)"')

    def extract_description(self, response):
        css = '.ProductDescription__LongDescription-sc-19e216s-5::text'
        description = response.css(css).extract_first()
        return [des.strip() for des in description.split('.') if des.strip()] if description else []

    def extract_name(self, response):
        return response.css('.ProductDetail__ProductName-rkmewc-6::text').extract_first()

    def extract_care(self, response):
        raw_care = response.xpath('//li[contains(.,"wash")]/text()').extract_first()
        return [care.strip() for care in raw_care.split('.')] if raw_care else []

    def extract_brand(self):
        return 'SAVAGE X FENTY'

    def extract_categories(self, response):
        trail = response.meta.get('trail', [])
        return [c for c, _ in trail]

    def extract_image_urls(self, response):
        return response.css('.ProductImageCarousel__ImageCarousel-x1qgfw-7 img::attr(src)').extract()

    def extract_skus(self, response):
        skus = {}
        common_sku = extract_price_details(self.extract_price(response))
        raw_skus = self.extract_raw_skus(response)

        for raw_sku in raw_skus:
            for size in raw_sku['product_id_object_list']:
                sku = common_sku.copy()
                sku['colour'] = raw_sku['color']
                sku['size'] = size['label_instance']

                if size['availability'] != 'in stock':
                    sku['out_of_stock'] = True

                skus[f"{sku['colour']}_{sku['size']}"] = sku

        return skus

    def extract_raw_skus(self, response):
        xpath = "//script[contains(., 'related_product_id_object_list')]/text()"
        pattern = '"initialProps":{"product".*related_product_id_object_list":(\[.*]),"available_quantity_master'
        raw_skus = response.xpath(xpath).re_first(pattern)
        return json.loads(raw_skus)

    def extract_market(self):
        return 'UK'

    def extract_gender(self):
        return 'Women'

    def extract_price(self, response):
        return response.css('.ProductDetail__PriceContainer-rkmewc-15 span::text').extract()

    def extract_retailer(self):
        return 'savagex'

    def extract_currency(self):
        return 'GBP'


class SavagexSpider(CrawlSpider):
    name = 'savagex-crawl-spider'
    allowed_domains = ['www.savagex.co.uk']
    start_urls = ['https://www.savagex.co.uk/']
    product_parser = ProductParser()

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 '
                      'Safari/537.36',
    }

    product_css = ['.NavBar__Wrapper-dkj1li-0.ezwYuW', '.HoverMenu__SubmenuWrapper-um7uz7-2',
                   '.ProductBrowserSidebar__Subcategories-s1ty7diy-2.KAtHz', '.HoverMenu__Wrapper-um7uz7-0',
                   '.ProductBrowserSidebar__Wrapper-sc-1ty7diy-0', '.FirstLookLayout__PanelColumns-sc-48pbor-1']
    listing_css = ['.ProductGrid__Container-s3uyfmk-0.hrqmNO', '.ProductGrid__Container-sc-3uyfmk-0', '.slick-slider']
    rules = [
        Rule(LinkExtractor(restrict_css=product_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_item')
    ]

    def parse(self, response):
        meta = {'trail': self.extract_trail(response)}
        page_urls = response.xpath("//text()").re('"pageUrl":"(.*?)"')
        for url in page_urls:
            yield Request(response.urljoin(url), callback=self.parse_page_urls, meta=meta.copy())

    def parse_page_urls(self, response):
        meta = {'trail': self.extract_trail(response)}
        for request in super().parse(response):
            request.meta['trail'] = meta['trail']
            yield request

    def parse_item(self, response):
        return self.product_parser.parse(response)

    def extract_trail(self, response):
        title = self.extract_title(response)
        trail = response.meta.get('trail', [])
        if title:
            trail = trail + [[title, response.url]]

        return trail

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        if title:
            title = title.split('|')[0].strip()

        return title
