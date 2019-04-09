from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from whitestuff_crawler.items import WhitestuffCrawlerItem, ProductLoader
import scrapy
import json
import re


class WhiteStuffSpider(CrawlSpider):
    name = 'white_stuff_spider'
    start_urls = ['https://www.whitestuff.com/']
    category_css = '.navbar-subcategory__item'
    product_css = '.seoworkaround'
    currency = ''
    gender = ("womens", "mens", "kids")
    allow_links = ('/womens', '/mens', '/kids', '/linen-shop', 'accessories-and-shoes', '/sale')

    rules = (
        Rule(LinkExtractor(allow=allow_links, restrict_css=category_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        product = self.parse_info(response)
        skus_url = response.css('.product-form > form > script::attr(src)').get()
        return scrapy.Request(skus_url, meta={"product": product}, callback=self.parse_skus)

    def parse_info(self, response):
        product = ProductLoader(item=WhitestuffCrawlerItem(), response=response)
        product.add_css('pid', '.product-info__product-id > span::text')
        product.add_value('gender', self.product_gender(response))
        product.add_css('category', '.breadcrumb-list__item > a::text')
        product.add_value('brand', 'White Stuff')
        product.add_value('url', response.url)
        product.add_css('name', '.product-info__heading::text')
        product.add_css('description', '.product-info__desc.js-lineclamp::text')
        product.add_css('care', '.ish-ca-value::text')
        product.add_css('image_urls', '.product-image__main  img::attr(src)')
        self.currency = self.product_currency(response)
        return product.load_item()

    def parse_skus(self, response):
        product = response.meta['product']
        product['skus'] = self.skus(response)
        return product

    def product_currency(self, response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').get()

    def product_gender(self, response):
        categories = response.css('.breadcrumb-list__item > a::text').getall()
        category = " ".join(categories)
        return [gender for gender in self.gender if gender in category.lower()]

    def skus(self, response):
        product_detail = []

        response_json = response.text.split('=')[1][:-1]
        response_json = re.sub('\n | //this is temporary until the feature is supported in the backoffice', '',
                               response_json)
        response_json = re.sub(r"\\", "'", response_json)
        response_json = json.loads(response_json)
        product_variations = response_json['productVariations']

        for skus_key in product_variations:
            skus = product_variations[skus_key]
            product = {
                'color': skus['colour'],
                'size': skus['size'],
                'skus_id': skus['colour'] + "_" + skus["size"],
                'currency': self.currency,
                'out_of_stock': skus['inStock'],
                'price': skus['salePrice']
            }
            if skus['salePrice'] != skus['listPrice']:
                product.update({'previous_price': skus['listPrice']})

            product_detail.append(product)

        return product_detail

