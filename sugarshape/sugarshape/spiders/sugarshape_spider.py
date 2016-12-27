import re
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from sugarshape.items import SugarshapeItem


class SugarShapeSpider(CrawlSpider):
    name = "sugarshape"
    allowed_domains = ["sugarshape.de"]
    start_urls = [
        "http://sugarshape.de/shop",
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=['#SusCategoryBox', 'div.pager'])),
        Rule(LinkExtractor(restrict_css=['#SusGridProductTitle', '#SusCategoryGridImage']), callback='parse_items')
    )

    CURRENCY = "EUR"

    def parse_items(self, response):
        garment = SugarshapeItem()
        garment['retailer'] = 'sugarshape'
        garment['market'] = 'DE'
        garment['lang'] = 'de'
        garment['gender'] = 'women'
        garment['name'] = response.css('#productTitle span::text').extract_first()
        garment['brand'] = 'Sugar Shape'
        garment['description'] = response.css('#description p::text').extract()
        garment['category'] = response.css('#breadCrumb a:last-child::text').extract_first()
        garment['url'] = response.url
        garment['industry'] = None
        garment['currency'] = self.CURRENCY
        garment['image_urls'] = response.css('a[id ^="morePics"]::attr(href)').extract()
        garment['spider_name'] = self.name
        garment['price'] = self.product_price(response)
        garment['url_original'] = response.url
        garment['care'] = self.product_care(response)
        garment['skus'] = self.get_skus(response)
        garment['retailer_sku'] = self.retailer_sku(response)

        return garment

    def product_color(self, response):
        description_lines = self.product_description(response)
        color_pattern = '^farbe: (.*)'
        matches = filter(lambda line: re.match(color_pattern, line.strip().lower()), description_lines)
        if matches:
            color = re.match(color_pattern, matches[0].strip().lower()).group(1).strip()
            return color

        return None

    def product_care(self, response):
        description_lines = self.product_description(response)
        care_pattern = '^Material: (.*)'
        matches = filter(lambda line: re.match(care_pattern, line.strip()), description_lines)
        if matches:
            care = re.match(care_pattern, matches[0].strip()).group(1)
            return care

        return None

    def product_description(self, response):
        return response.css('div#description > p::text').extract()

    def product_price(self, response):
        price = response.css('#productPrice div:nth-child(1)::text').extract_first()
        price = ''.join(price.strip().split(' ')[0].split(','))
        return price

    def product_sizes(self, response):
        return response.css('a.variantSelector::text').extract()

    def retailer_sku(self, response):
        scripts = response.css('script::text').extract()
        pattern = '_shopgate.item_number = "(\d+)"'
        regex = re.compile(pattern)
        retailer_sku = [m.group(1) for s in scripts for m in [regex.search(s)] if m][0]
        return retailer_sku

    def get_skus(self, response):
        sizes = self.product_sizes(response)
        price = self.product_price(response)
        color = self.product_color(response)
        return map(lambda size: {
            'price': price,
            'currency': self.CURRENCY,
            'color': color,
            'size': size
        }, sizes)
