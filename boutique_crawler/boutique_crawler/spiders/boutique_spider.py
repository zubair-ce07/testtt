import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import datetime
import json
from boutique_crawler.items import BoutiqueCrawlerItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class BoutiqueSpider(scrapy.spiders.CrawlSpider):
    name = 'boutique_spider'
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
        return scrapy.Request(url, meta=product, callback=self.image_urls)

    def parse_info(self, response):
        item = ItemLoader(item=BoutiqueCrawlerItem(), response=response)
        item.default_output_processor = TakeFirst()
        item.description_out = list
        item.skus_out = list

        item.add_css('pid', '.wishl-add-wrapper::attr(data-product-id)')
        item.add_value('gender', 'female')
        item.add_value('url', response.url)
        item.add_value('date', str(datetime.datetime.now()))
        item.add_css('name', '.product-heading__title.product-title::text')
        item.add_value('description', self.product_description(response))
        item.add_value('image_url', '')
        item.add_value('skus', self.skus(response))
        return item.load_item()

    def image_urls(self, response):
        product = response.meta
        src = []
        data = json.loads(response.text)

        for images in data['product']['images']:
            src.append(images['src'])

        product['image_url'] = src
        return product

    def product_description(self, response):
        description = []
        product_descriptions = response.css('.product__specs-detail *::text').getall()

        for desc in product_descriptions:
            description.append((desc.strip()))
        return description

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
