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


class GymboreeParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    UNWANTED_TOKENS = {'toy', 'toys'}
    price_x = "//span[@class='price']//text()|//span[" \
              "@class='oldPrice']//text()"

    GENDER_MAP = [('herren', 'boys'), ('damen', 'girls'), ]

    def parse(self, response):
        if '/error_general' in response.url:
            return
        hxs = response
        product_components = self.product_title(hxs)
        product_brand, product_name = product_components[0], product_components[1]
        if not product_name:
            self.logger.info('Not a product page %s' % response.url)
            return
        description = self.product_description(hxs)
        categories = self.product_category(hxs)
        tokens = tokenize(categories)
        if tokens & self.UNWANTED_TOKENS:
            self.logger.info('Drop unwanted item %s' % response.url)
            return

        common = {
            'brand': self.retailer,
            'category': categories,
            'care': '',
            'description': description,
            'gender': self.product_gender(tokens),
            'name': product_name,
            'brand': product_brand,
            'market': self.market
        }
        currency_path = 'div.prod_block meta[itemprop=priceCurrency]::attr(' \
                        'content)'
        hxs.meta['currency'] = hxs.css(currency_path).extract_first()
        hxs.meta['common'] = common
        hxs.meta['remaining_clr_req'] = hxs.css('div.col_sel li>'
                                                'a::attr(href)').extract()
        return self.parse_color_variant(hxs)

    def parse_color_variant(self, hxs):
        product_id = self.product_id(hxs)
        garment = self.new_unique_garment(product_id)
        self.boilerplate_minimal(garment, hxs)
        garment.update(hxs.meta['common'])
        garment['image_urls'] = self.image_urls(hxs)
        skus = self.skus(hxs, product_id)
        if skus:
            garment['skus'] = skus
        else:
            garment['out_of_stock'] = True
        if hxs.meta['remaining_clr_req']:
            next_req = hxs.meta['remaining_clr_req'].pop()
            yield Request(next_req, meta=hxs.meta,
                          callback=self.parse_color_variant)
        yield garment

    def product_id(self, hxs):
        return hxs.css('div.prod_block div.visible-lg>p::text').extract_first(
        ).split('.:')[1]

    def product_title(self, hxs):
        return hxs.css('h1.visible-lg[itemprop]::text')\
            .extract_first().split('-')

    def product_description(self, hxs):
        return hxs.css('div.prod_block div.visible-lg ul '
                       'label::text').extract()

    def product_category(self, hxs):
        return hxs.css('.detail_bread2>li>a>font::text').extract()

    def product_gender(self, tokens):
        for token, gender in self.GENDER_MAP:
            if token in tokens:
                return gender
        return 'unisex-kids'

    def product_color(self, product_title):
        title_components = product_title.split('-')
        return title_components[len(title_components)-1]

    def skus(self, hxs, product_id):
        skus = {}
        common = {
            'colour': self.product_color(hxs.meta['common']['name']),
            'currency': hxs.meta['currency'],
        }
        for size_var in hxs.css('div.size_info li>a'):
            size_id = size_var.css('::attr(data-selection-id)').extract_first()
            skus[str(product_id+size_id)] = sku = common.copy()
            sku['size'] = size_var.css('span::text').extract_first().strip()
            previous_price, price, currency = self.product_pricing(hxs)
            sku['price'] = price
            if previous_price:
                sku['previous_prices'] = previous_price
            if size_var.css('.no_stock'):
                # If no_stock class has been applied on the size then it
                # means that the give size is not available
                sku['out_of_stock'] = True
        return skus

    def image_urls(self, hxs):
        # Replace 87x87 image size with 380x340 for a full size image
        return [img.replace('87_87', '380_340') for img in hxs.css(
            'div.detailsInfo div.otherPictures img::attr(src)').extract()]


class SchuhcenterCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = GymboreeParseSpider()
    listings_c = ['div.flyoutholder article.main_categories ul a',
                  'div.pagenav.pull-right a.next']
    products_c = 'section.productlist div.over-links>a'
    rules = (
        Rule(LinkExtractor(restrict_css=listings_c), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_c), callback='parse_item'),
    )
