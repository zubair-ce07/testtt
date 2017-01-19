import re
import time
from scrapy.http.request.form import FormRequest
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider
from woolworths_za.items import WoolworthsItem


class WoolworthsSpider(CrawlSpider):
    name = "woolworths"
    allowed_domains = ["woolworths.co.za"]
    start_urls = ['http://www.woolworths.co.za/']
    product_filter = ['/Gifts',
                      '/Beauty',
                      '/Homeware',
                      '/Household',
                      '/Food',
                      '/Essentials',
                      '/Today-s-Deal'
                     ]
    rules = [
        Rule(LinkExtractor(restrict_css=[
            'div.horizontal-menu-container',
            'ul.nav-list--main',
            'ol.pagination__pages',
        ])),
        Rule(LinkExtractor(restrict_css='a.product-card__details',
                           deny=product_filter),
             callback='parse_item'),
    ]

    def parse_item(self, response):
        garment = WoolworthsItem()
        garment['name'] = self.product_name(response)
        garment['brand'] = self.product_brand(response)
        garment['category'] = self.product_category(response)
        garment['retailer'] = 'woolworths'
        garment['price'] = self.product_price(response)
        if self.is_sale(response):
            garment['previous_price'] = self.product_old_price(response)
        garment['currency'] = self.product_currency(response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.product_images(response)
        garment['description'] = self.product_description(response)
        garment['industry'] = None
        garment['market'] = 'ZA'
        garment['url'] = response.url
        garment['url_original'] = response.url
        garment['retailer_sku'] = self.product_retailer_sku(response)
        garment['care'] = self.product_care(response)
        garment['date'] = int(time.time())
        garment['skus'] = {}
        checklist = self.get_sku_checklist(response)
        return self.fetch_skus(garment, checklist)

    def product_name(self, response):
        selector = 'meta[itemprop="name"]::attr(content)'
        return response.css(selector).extract_first()

    def product_brand(self, response):
        selector = 'meta[itemprop="brand"]::attr(content)'
        return response.css(selector).extract_first()

    def product_category(self, response):
        selector = 'li.breadcrumb__crumb a::text'
        return response.css(selector).extract()

    def product_currency(self, response):
        selector = 'meta[itemprop="priceCurrency"]::attr(content)'
        return response.css(selector).extract_first()

    def product_description(self, response):
        selector = 'meta[itemprop="description"]::attr(content)'
        return response.css(selector).extract()

    def product_retailer_sku(self, response):
        selector = 'meta[itemprop="productId"]::attr(content)'
        return response.css(selector).extract_first()

    def product_color(self, response):
        selector = 'meta[itemprop="color"]::attr(content)'
        return response.css(selector).extract_first().strip()

    def get_sku_checklist(self, response):
        color_elems = response.css('img.colour-swatch')
        size_elems = response.css('a.product-size')
        colors = []
        for elem in color_elems:
            onclick = elem.css('::attr(onclick)').extract_first()
            colors += [
                {
                    'title': elem.css('::attr(title)').extract_first(),
                    'id'   : re.findall('changeMainProductColour\((\d+)', onclick)[0]
                }
            ]
        sizes = []
        for elem in size_elems:
            onclick = elem.css('::attr(onclick)').extract_first()
            sizes += [
                {
                    'title': elem.css('::text').extract_first(),
                    'id'   : re.findall('changeMainProductSize\(\d+,(\d+)', onclick)[0]
                }
            ]

        return [(color, size) for color in colors for size in sizes]

    def get_skus(self, garment, checklist):
        color, size = checklist.pop()
        price_url = 'http://www.woolworths.co.za/store/fragments/product-common/ww/price.jsp'
        return FormRequest(url=price_url,
                           formdata={'productItemId': garment['retailer_sku'],
                                     'colourSKUId': color['id'],
                                     'sizeSKUId': size['id'],
                                     },
                           callback=self.parse_price,
                           meta={'garment': garment,
                                 'checklist': checklist,
                                 'color': color,
                                 'size': size,
                                 }
                           )

    def parse_price(self, response):
        checklist = response.meta['checklist']
        garment = response.meta['garment']
        self.make_sku(response)
        return self.fetch_skus(garment, checklist)

    def fetch_skus(self, garment, checklist):
        if checklist:
            return self.get_skus(garment, checklist)
        else:
            return garment

    def price_from_ajax(self, response):
        price_css = 'span.price::text'
        return int(response.css(price_css).re_first('[\d|\.]+').replace('.', ''))

    def make_sku(self, response):
        garment = response.meta['garment']
        color = response.meta['color']
        size = response.meta['size']
        price = self.price_from_ajax(response)
        currency = garment['currency']
        skus = garment['skus']
        sku_id = color['title'].replace(' ', '_') + '_' + size['title']
        skus[sku_id] = {
            'color': color['title'],
            'size': size['title'],
            'price': price,
            'currency': currency,
        }

    def product_price(self, response):
        selector = 'meta[itemprop="price"]::attr(content)'
        return int(response.css(selector).extract_first().replace('.',''))

    def product_old_price(self, response):
        selector = 'span.price--original::text'
        return int(response.css(selector).re_first('[\d|\.]+').replace('.',''))

    def product_images(self, response):
        selector = 'a[data-gallery-full-size]::attr(data-gallery-full-size)'
        return ['http://' + link.lstrip('/') for link in response.css(selector).extract()]

    def is_sale(self, response):
        return response.css('span.price--discounted')

    def product_care(self, response):
        desc = self.product_description(response)
        pattern = re.compile('\d+%.*$', re.MULTILINE)
        for line in desc:
            return re.findall(pattern, line)

    def product_gender(self, response):
        patterns = [
            ('men', '/Men'),
            ('women', '/Women'),
            ('boys', '/Boys'),
            ('girls', '/Girls'),
            ('unisex', '/Unisex'),
            ('unisex-kids', '/School-Uniform'),
        ]

        for gender, gender_pattern in patterns:
            if gender_pattern in response.url:
                return gender
