# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, tokenize
from scrapy import Request


class Mixin(object):
    market = 'DE'
    retailer = 'schuhcenter'
    allowed_domains = ['www.schuhcenter.de']
    start_urls = [
        'http://www.schuhcenter.de/'
    ]


class SchuhcenterParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    price_x = "//span[@class='price']//text()|//span[" \
              "@class='oldPrice']//text()"

    GENDER_MAP = [('herren', 'boys'), ('damen', 'girls'), ]

    def parse(self, response):
        if '/error_general' in response.url:
            return
        product_components = self.product_title(response)
        product_brand, product_name = product_components[0], product_components[1]
        if not product_name:
            self.logger.info('Not a product page %s' % response.url)
            return
        categories = self.product_category(response)
        tokens = tokenize(categories)
        common = {
            'brand': self.retailer,
            'category': self.product_category(response),
            'care': '',
            'description': self.product_description(response),
            'gender': self.product_gender(tokens),
            'name': product_name,
            'brand': product_brand,
            'market': self.market
        }
        currency_path = 'div.prod_block meta[itemprop=priceCurrency]::attr(' \
                        'content)'
        response.meta['currency'] = response.css(currency_path).extract_first()
        response.meta['common'] = common
        response.meta['remaining_clr_req'] = response.css('div.col_sel li>'
                                                'a::attr(href)').extract()
        return self.parse_color_variant(response)

    def parse_color_variant(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        self.boilerplate_minimal(garment, response)
        garment.update(response.meta['common'])
        garment['image_urls'] = self.image_urls(response)
        skus = self.skus(response, product_id)
        if skus:
            garment['skus'] = skus
        else:
            garment['out_of_stock'] = True
        if response.meta['remaining_clr_req']:
            # Request for the remaining colors of the product
            next_req = response.meta['remaining_clr_req'].pop()
            yield Request(next_req, meta=response.meta,
                          callback=self.parse_color_variant)
        yield garment

    def product_id(self, response):
        return response.css('div.prod_block div.visible-lg>p::text').extract_first(
        ).split('.:')[1]

    def product_title(self, response):
        return response.css('h1.visible-lg[itemprop]::text')\
            .extract_first().split('-')

    def product_description(self, response):
        return response.css('div.prod_block div.visible-lg ul '
                       'label::text').extract()

    def product_category(self, response):
        return response.css('.detail_bread2>li>a>font::text').extract()

    def product_gender(self, tokens):
        for token, gender in self.GENDER_MAP:
            if token in tokens:
                return gender
        return 'unisex-kids'

    def product_color(self, product_title):
        title_components = product_title.split('-')
        return title_components[len(title_components)-1]

    def skus(self, response, product_id):
        skus = {}
        common = {
            'colour': self.product_color(response.meta['common']['name']),
            'currency': response.meta['currency'],
        }
        for size_var in response.css('div.size_info li>a'):
            size_id = size_var.css('::attr(data-selection-id)').extract_first()
            skus[str(product_id+size_id)] = sku = common.copy()
            sku['size'] = size_var.css('span::text').extract_first().strip()
            previous_price, price, currency = self.product_pricing(response)
            sku['price'] = price
            if previous_price:
                sku['previous_prices'] = previous_price
            if size_var.css('.no_stock'):
                # If no_stock class has been applied on the size then it
                # means that the give size is not available
                sku['out_of_stock'] = True
        return skus

    def image_urls(self, response):
        # Replace 87x87 image size with 380x340 for a full size image
        return [img.replace('87_87', '380_340') for img in response.css(
            'div.detailsInfo div.otherPictures img::attr(src)').extract()]


class SchuhcenterCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = SchuhcenterParseSpider()
    listings_c = ['div.flyoutholder article.main_categories ul a',
                  'div.pagenav.pull-right a.next']
    products_c = 'section.productlist div.over-links>a'
    rules = (
        Rule(LinkExtractor(restrict_css=listings_c), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_c), callback='parse_item'),
    )
