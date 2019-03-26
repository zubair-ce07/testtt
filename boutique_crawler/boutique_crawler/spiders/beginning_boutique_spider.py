import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import datetime
import json
from boutique_crawler.items import BoutiqueCrawlerItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class BeginningBoutiqueSpider(scrapy.spiders.CrawlSpider):
    name = 'beginning_boutique_spider'
    start_urls = ['https://www.beginningboutique.com.au/']

    category_css = [
        '.site-nav__link.site-nav__link--primary',
        '.site-nav__link.site-nav__link--type'
    ]
    product_css = [
        '.product-card-image-wrapper',
        '.product-title.product-card__title'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=category_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        product = self.parse_info(response)
        url = product['url'] + '.json?'
        return scrapy.Request(url, meta={"product": product}, callback=self.image_urls)

    def parse_info(self, response):
        item = ItemLoader(item=BoutiqueCrawlerItem(), response=response)
        item.default_output_processor = TakeFirst()
        item.description_in = MapCompose(str.strip)
        item.description_out = list
        item.care_in = MapCompose(str.strip)
        item.skus_out = list
        item.category_out = list

        item.add_css('pid', '.wishl-add-wrapper::attr(data-product-id)')
        item.add_value('gender', 'female')
        item.add_value('url', response.url)
        item.add_value('date', str(datetime.datetime.now()))
        item.add_css('name', '.product-heading__title.product-title::text')
        item.add_xpath('description',
                       '//ul[@class="product__specs-list"]/li[1]/div[@class="product__specs-detail"]/text()')
        item.add_xpath('description',
                       '//ul[@class="product__specs-list"]/li[1]/div[@class="product__specs-detail"]/p/text()')
        item.add_xpath('care', '//ul[@class="product__specs-list"]/li[2]/div[@class="product__specs-detail"]/text()')
        url = response.url
        item.add_value('category', url.split('/')[3:])
        item.add_value('skus', self.skus(response))
        return item.load_item()

    def image_urls(self, response):
        product = response.meta['product']
        response_details = json.loads(response.text)

        product['image_urls'] = [image['src'] for image in response_details['product']['images']]
        return product

    def product_price(self, response):
        price_list = response.css('.product__price.product-price *::text').getall()
        return [price for price in price_list if '$' in price]

    def skus(self, response):
        product_detail = []
        product = {}

        price = self.product_price(response)
        currency = response.css('meta[itemprop="priceCurrency"]::attr(content)').get()
        size_options = response.css('.input--full > option::text').getall()

        for sku_id in size_options:
            if len(price) > 1:
                product = {'previous price': price[1]}

            product.update({
                'price': price[0],
                'currency': currency,
                'size': sku_id,
                'sku_id': sku_id,
            })

            product_detail.append(product)
        return product_detail

