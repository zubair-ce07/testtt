import re
import json
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PuketSpider(CrawlSpider):

    name = "puket"
    allowed_domains = ['puket.com.br']
    rules = (
        Rule(LinkExtractor(allow='a.next'), callback='parse_product'),
    )

    def start_requests(self):
        yield scrapy.Request('http://www.puket.com.br/', callback=self.parse_menu)

    def parse_menu(self, response):
        menu_urls = response.css('div#topMenu a::attr(href)').extract()[:-3]
        for menu_url in menu_urls:
            yield scrapy.Request(url=menu_url, callback=self.parse_product_category)

    def parse_product_category(self, response):
        category_urls = response.css('div.shelf-category-list a::attr(href)').extract()
        for category_url in category_urls:
            yield scrapy.Request(url=category_url, callback=self.parse_product)

    def parse_product(self, response):
        product_url = response.css('div.box-product a.shelf-url::attr(href)').extract_first()
        if product_url:
            yield response.follow(product_url, callback=self.parse_product_info)

    def parse_product_info(self, response):

        garment_skus = []
        trail = []

        def extract_with_css(selector):
            return response.css(selector).extract_first()

        def extract_all_with_css(selector):
            return response.css(selector).extract()

        visited_urls = response.css('.product-breadcrumb a::attr(href)').extract()
        for url in visited_urls:
            trail.append(response.urljoin(url))

        care = response.css('.descProduct::text').extract()[2:]
        if not care:
            care = response.css('.descProduct p::text').extract()[2:]

        puket_skus = response.css('script[xml\:space="preserve"]::text').extract_first()
        puket_skus = re.search('(skuJson = )(.*\n)*', puket_skus).group(0).split('skuJson = ')[1].rsplit(';', 1)[0]
        puket_skus = json.loads(puket_skus)

        for sku in puket_skus["skus"]:
            garment_skus.append({
                'sku_id': sku['sku'],
                'price': sku['bestPrice'],
                'previous_prices': sku['listPrice'],
                'currency': sku['currency'],
                'colour': sku['udas']['COR'],
                'size': sku['udas']['TAMANHO']
            })

        yield {
            'url': response.urljoin(puket_skus["product_url"]),
            'gender': puket_skus['udasProd']['google_gender'],
            'retailer_sku': puket_skus['productId'],
            'brand': puket_skus['udasProd']['marca'],
            'lang': extract_with_css('html::attr(lang)'),
            'name': extract_with_css('article.infoProduct .nameProduct::text'),
            'price': extract_with_css('.bestPrice .val::attr(content)'),
            'currency': extract_with_css('[itemprop="priceCurrency"]::attr(content)'),
            'care': care,
            'category': extract_all_with_css('div.product-breadcrumb > a::text')[1:],
            'trail': trail,
            'image_urls': extract_all_with_css('ul.list-thumbs a::attr(href)'),
            'skus': garment_skus
        }
