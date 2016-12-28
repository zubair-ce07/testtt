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

    def parse_items(self, response):
        garment = SugarshapeItem()
        garment['retailer'] = 'sugarshape'
        garment['market'] = 'DE'
        garment['lang'] = 'de'
        garment['gender'] = 'women'
        garment['name'] = response.css('#productTitle span::text').extract_first()
        garment['brand'] = 'Sugar Shape'
        garment['description'] = self.product_description(response)
        garment['category'] = response.css('#breadCrumb a:last-child::text').extract()
        garment['url'] = response.url
        garment['industry'] = None
        garment['currency'] = self.product_currency(response)
        garment['image_urls'] = response.css('a[id ^="morePics"]::attr(href)').extract()
        garment['spider_name'] = self.name
        garment['price'] = self.product_price(response)
        garment['url_original'] = response.url
        garment['care'] = self.product_care(response)
        garment['skus'] = self.get_skus(response)
        garment['retailer_sku'] = self.retailer_sku(response)

        return garment

    def product_color(self, response):
        color_pattern = 'Farbe:?[\s]*([\S]+)'
        colors = response.css("div#description p:contains('Farbe:')").re(color_pattern)
        return colors[0]

    def product_care(self, response):
        description_lines = self.product_description(response)
        matches = filter(lambda line: line.strip().startswith('Material'), description_lines)
        return matches[0]

    def product_description(self, response):
        return response.css('div#description > p::text').extract()

    def product_price(self, response):
        price = response.css('#productPrice div:nth-child(1)::text').extract_first()
        price = ''.join(price.strip().split(' ')[0].split(','))
        return price

    def product_sizes(self, response):
        return response.css('a.variantSelector::text').extract()

    def retailer_sku(self, response):
        id_pattern = "prodId(?:[\s]*)?=(?:[\s]*)?'(.*)'"
        ids = response.css("script:contains('var prodId')").re(id_pattern)
        return ids[0]

    def get_skus(self, response):
        sizes = self.product_sizes(response)
        price = self.product_price(response)
        color = self.product_color(response)
        currency = self.product_currency(response)

        skus = {}
        for size in sizes:
            sku = {
                'price': price,
                'currency': currency,
                'size': size,
            }
            if color:
                sku['color'] = color

            sku_id = color + '_' + size if color else size
            skus[sku_id] = sku

        return skus

    def product_currency(self, response):
        currency_pattern = "currency:(?:\s*)'([A-Za-z]*)'"
        currencies = response.css("script:contains('currency:')").re(currency_pattern)
        return currencies[0]
