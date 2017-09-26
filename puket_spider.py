import re
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PuketSpider(CrawlSpider):

    name = "puket"
    allowed_domains = ['puket.com.br']
    start_urls = ['http://www.puket.com.br/']
    rules = (
        Rule(LinkExtractor(restrict_css=('#topMenu a', '.shelf-category-list a', 'a.next')), follow=True),
        Rule(LinkExtractor(restrict_css=('a.shelf-url',)), callback='parse_product'),
    )
    puket_skus = {}

    def product_skus(self):
        skus = {}
        for sku in self.puket_skus["skus"]:
            sku_id = sku['sku']
            skus[sku_id] = {
                'price': sku['bestPrice'],
                'previous_prices': sku['listPrice'],
                'currency': sku['currency'],
                'colour': sku['udas']['COR'],
                'size': sku['udas']['TAMANHO']
            }
        return skus

    def product_care(self):
        care = self.puket_skus.get('udasProd').get('composicao', None)
        if care:
            cares = care.split('<br>')
            care = list(filter(None, cares))
        return care

    def product_gender(self):
        return self.puket_skus.get('udasProd').get('google_gender', None)

    def product_brand(self):
        return self.puket_skus.get('udasProd').get('marca', None)

    def read_puket_skus(self, response):
        puket_skus_response = response.css('script[xml\:space="preserve"]::text').extract_first()
        puket_skus_json = re.search("(?s)var\s+skuJson\s*=\s*(\{.*?\});", puket_skus_response)
        puket_skus_json = puket_skus_json.group(1)
        self.puket_skus = json.loads(puket_skus_json)

    def product_trail(self, response):
        trail = []
        visited_urls = response.css('.product-breadcrumb a::attr(href)').extract()
        for url in visited_urls:
            trail.append(response.urljoin(url))
        return trail

    def product_url(self, response):
        return response.urljoin(self.puket_skus["product_url"])

    def product_language(self, response):
        return response.css('html::attr(lang)').extract_first()

    def product_name(self, response):
        return response.css('.infoProduct .nameProduct::text').extract_first()

    def product_price(self, response):
        return response.css('.bestPrice .val::attr(content)').extract_first()

    def product_currency(self, response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()

    def product_categories(self, response):
        return response.css('.product-breadcrumb a::text').extract()[1:]

    def product_image_urls(self, response):
        return response.css('.list-thumbs a::attr(href)').extract()

    def parse_product(self, response):

        garment = {}

        self.read_puket_skus(response)

        garment['retailer_sku'] = self.puket_skus['productId']
        garment['care'] = self.product_care()
        garment['skus'] = self.product_skus()
        garment['brand'] = self.product_brand()
        garment['gender'] = self.product_gender()
        garment['trail'] = self.product_trail(response)
        garment['url'] = self.product_url(response)
        garment['lang'] = self.product_language(response)
        garment['name'] = self.product_name(response)
        garment['price'] = self.product_price(response)
        garment['currency'] = self.product_currency(response)
        garment['category'] = self.product_categories(response)
        garment['image_urls'] = self.product_image_urls(response)
        return garment
