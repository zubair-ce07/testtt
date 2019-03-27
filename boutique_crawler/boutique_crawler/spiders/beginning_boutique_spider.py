import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import datetime
import json
from boutique_crawler.items import BoutiqueCrawlerItem, ProductLoader


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
        product = ProductLoader(item=BoutiqueCrawlerItem(), response=response)
        product.add_css('pid', '.wishl-add-wrapper::attr(data-product-id)')
        product.add_value('gender', 'female')
        product.add_value('url', response.url)
        product.add_value('date', str(datetime.datetime.now()))
        product.add_css('name', '.product-heading__title.product-title::text')
        product.add_css('description', '.product__specs-list li:contains(DESCRIPTION) > .product__specs-detail::text')
        product.add_css('description',
                        '.product__specs-list li:contains(DESCRIPTION) > .product__specs-detail > p::text')
        product.add_css('care', '.product__specs-list li:contains(FABRICATION) > .product__specs-detail::text')
        url = response.url
        product.add_value('category', url.split('/')[3:])
        product.add_value('skus', self.skus(response))
        return product.load_item()

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

