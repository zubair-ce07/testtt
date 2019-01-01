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

    def extract_description(self, response):
        description = response.css('.product-details .tab-content::text').extract_first()
        return [des.strip() for des in description.split('.') if des.strip()]

    def extract_image_urls(self, response):
        return response.css('.productcarouselslides img::attr(data-image-replacement)').extract()

    def extract_skus(self, response):
        skus, price = [], []
        price.append(self.extract_previous_price(response))
        price.append(self.extract_price(response))
        price.append(self.extract_currency(response))
        price_details = extract_price_details(price)

        item = {}
        colours_data = response.css('.swatches.color a::text').extract()
        size_options = response.css('.swatches.size .emptyswatch a::text').extract()
        item['color'] = [color.strip() for color in colours_data]
        item.update(price_details)

        for option in size_options:
            size_option = item.copy()
            size_option['size'] = option.strip()
            size_option['sku_id'] = f"{item['color'][0]}_{option.strip()}"
            skus.append(size_option)

        return skus

    def extract_currency(self, response):
        return response.xpath("//script[contains(., 'productObj')]/text()").re('currencyCode":"(.*?)"')[0]

    def extract_category(self, response):
        return response.xpath("//script[contains(., 'productObj')]/text()").re('category":"(.*?)"')[0]

    def extract_market(self):
        return 'EU'

    def extract_brand(self, response):
        return response.xpath("//script[contains(., 'productObj')]/text()").re('brand":"(.*?)"')[0]

    def extract_retailer(self):
        return 'wefashion.de'

    def extract_price(self, response):
        return response.xpath("//script[contains(., 'productObj')]/text()").re('price":"(.*?)"')[0]

    def extract_previous_price(self, response):
        previous_price = response.css('.price-standard::text').extract_first()
        if previous_price:
            previous_price = previous_price.replace('€', '').replace(',', '.').strip()
        return previous_price

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
        return title.split('|')[0] if title else title
