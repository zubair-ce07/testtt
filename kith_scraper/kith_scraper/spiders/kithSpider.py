import re

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule

from kith_scraper.items import KithItem


class KithSpider(CrawlSpider):
    name = "kith"
    start_urls = ['https://kith.com']
    allowed_domains = ['kith.com']
    allowed_url_patterns = ('\/pages\/women',
                            '\/pages\/kids',
                            '\/collections\/\.+\/mens',  # brand links for men
                            '\/collections\/.+\/wmns',  # brand links for momen
                            '\/collections\/kids-latest',  # kids page contains all items
                            )
    rules = (
        Rule(LinkExtractor(allow=allowed_url_patterns)),
        Rule(LinkExtractor(allow='.+\/products\/.+', ), callback='parse_item'),
    )

    def parse_item(self, response):
        item = KithItem()
        item['brand'] = self.get_brand(response)
        item['category'] = self.get_category(response)
        item['description'] = self.get_description(response)
        item['gender'] = self.get_gender(response)
        item['image_url'] = self.get_image_urls(response)
        item['name'] = self.get_name(response, item['brand'])
        item['retailer'] = self.get_retailer(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['skus'] = self.get_skus(response)
        item['url'] = response.url

        yield item

    def get_skus(self, response):
        product_skus = {}
        color = self.get_color(response)
        currency = self.get_currency(response)
        price = self.get_price(response)

        regex = '{"id":(\d+),"title":"([0-9]*\.?[0-9]*|\w+)".*?available":(.*?),"name.*?}'
        raw_skus = response.css('script').re(regex)
        for sku, size, availability in zip(raw_skus[0::3], raw_skus[1::3], raw_skus[2::3]):
            product_skus[sku] = {'color': color,
                                 'currency': currency,
                                 'price': price,
                                 'size': size,
                                 'availability': availability,
                                 }

        return product_skus

    def get_description(self, response):
        descriptions = response.css('.product-single-details-rte p::text').extract()
        descriptions = [desc.strip() for desc in descriptions]
        descriptions = list(filter(None, descriptions))
        return descriptions

    def get_category(self, response):
        return '/'.join(response.css('.breadcrumb a::text').extract()[1:])

    def get_image_urls(self, response):
        raw_urls = response.css(".super-slider-photo-img::attr(src)").extract()
        image_urls = [url.strip('/') for url in raw_urls]
        return image_urls

    def get_brand(self, response):
        return response.css("script.analytics::text").re_first('"brand":"(.*?)"')

    def get_name(self, response, brand):
        product_title = response.css('.product-header-title span::text').extract_first()
        brand_pattern = re.compile(re.escape(brand), re.IGNORECASE)
        name = brand_pattern.sub('', product_title)
        return name

    def get_color(self, response):
        return response.css('.-variant::text').extract_first().strip()

    def get_price(self, response):
        return response.css("script.analytics::text").re_first('"price":"([0-9]*\.?[0-9]*)"')

    def get_currency(self, response):
        return response.css("script.analytics::text").re_first('"currency":"(\w+)"')

    def get_retailer_sku(self, response):
        return response.css("script.analytics::text").re_first('"productId":(\d+)')

    def get_retailer(self, response):
        return 'kith-us'

    def get_style(self, response):
        return response.css('.product-single-details-rte p::text').re('Style: (.*)')

    def get_gender(self, response):
        if 'wmns' in response.url:
            return 'Women'
        if 'kidset' in response.url:
            return 'Kids'
        return 'Men'
