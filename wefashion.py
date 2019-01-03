from scrapy import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from item_structure import Item
from helpers import extract_price_details


class ProductParser(Spider):
    def __init__(self):
        self.seen_ids = set()

    def parse(self, response):
        item = Item()
        product_id = self.extract_product_id(response)

        if not self.is_new_item(product_id):
            return

        item['name'] = self.extract_name(response)
        item['retailer_sku'] = product_id
        item['spider_name'] = 'wefashion'
        item['brand'] = self.extract_brand(response)
        item['care'] = self.extract_care(response)
        item['category'] = self.extract_category(response)
        item['market'] = self.extract_market()
        item['retailer'] = self.extract_retailer()
        item['url'] = response.url
        item['description'] = self.extract_description(response)
        item['skus'] = self.extract_skus(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['trail'] = response.meta.get('trail', [])

        return item

    def is_new_item(self, product_id):
        if product_id and product_id not in self.seen_ids:
            self.seen_ids.add(product_id)
            return True

        return False

    def extract_product_id(self, response):
        return response.css('[id="pid"]::attr(value)').extract_first()

    def extract_name(self, response):
        return response.css('.product-name::text').extract_first().strip()

    def extract_care(self, response):
        care = response.css('.washingInstructions::text').extract()
        return [cr.strip() for cr in care if cr.strip()]

    def extract_description(self, response):
        description = response.css('.product-details .tab-content::text').extract_first()
        return [des.strip() for des in description.split('.') if des.strip()]

    def extract_image_urls(self, response):
        return response.css('.productcarouselslides img::attr(data-image-replacement)').extract()

    def extract_skus(self, response):
        skus = {}
        price = self.extract_price(response)
        common_sku = extract_price_details(price)
        raw_skus = response.css('.swatches.size .emptyswatch a::text').extract()
        sku_colors = response.css('.swatches.color a::text').extract()

        for raw_sku in raw_skus:
            for sku_color in sku_colors:
                sku = common_sku.copy()
                sku['color'] = sku_color.strip()
                sku['size'] = raw_sku.strip()
                sku['sku_id'] = f"{sku['color']}_{sku['size']}"
                skus[sku['sku_id']] = sku

        return skus

    def extract_category(self, response):
        xpath = "//script[contains(., 'productObj')]/text()"
        return response.xpath(xpath).re_first('category":"(.*?)"')

    def extract_market(self):
        return 'EU'

    def extract_brand(self, response):
        xpath = "//script[contains(., 'productObj')]/text()"
        return response.xpath(xpath).re_first('brand":"(.*?)"')

    def extract_retailer(self):
        return 'wefashion.de'

    def extract_price(self, response):
        price_map = response.css('.product-content .product-price div::text').extract()
        return [price.strip() for price in price_map if price.strip()]


class WeFashionSpider(CrawlSpider):
    name = 'wefashion-crawl-spider'
    allowed_domains = ['www.wefashion.de']
    start_urls = ['https://www.wefashion.de/']
    product_parser = ProductParser()

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36'
    }

    product_css = ['.level-top-1', '.category-refinement']
    listing_css = ['.container']
    rules = [
        Rule(LinkExtractor(restrict_css=product_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_item')
    ]

    def parse(self, response):
        title = self.extract_title(response)
        trail = response.meta.get('trail', [])
        trail = trail + [[title, response.url]]

        for request in super().parse(response):
            request.meta['trail'] = trail
            yield request

    def parse_item(self, response):
        return self.product_parser.parse(response)

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        return title.split('|')[0] or title
