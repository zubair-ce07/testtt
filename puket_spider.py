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
        Rule(LinkExtractor(restrict_css=('.box-product a.shelf-url',)), callback='parse_product'),
    )

    def parse_product(self, response):

        garment = {}

        def read_puket_skus():
            puket_skus_response = response.css('script[xml\:space="preserve"]::text').extract_first()
            puket_skus_json = re.search("(?s)var\s+skuJson\s*=\s*(\{.*?\});", puket_skus_response)
            puket_skus_json = puket_skus_json.group(1)
            puket_skus_ = json.loads(puket_skus_json)
            return puket_skus_

        puket_skus = read_puket_skus()

        def product_trail():
            trail = []
            visited_urls = response.css('.product-breadcrumb a::attr(href)').extract()
            for url in visited_urls:
                trail.append(response.urljoin(url))
            return trail

        def product_skus():
            skus = {}
            for sku in puket_skus["skus"]:
                sku_id = sku['sku']
                skus[sku_id] = {
                    'price': sku['bestPrice'],
                    'previous_prices': sku['listPrice'],
                    'currency': sku['currency'],
                    'colour': sku['udas']['COR'],
                    'size': sku['udas']['TAMANHO']
                }
            return skus

        def product_care():
            care = puket_skus.get('udasProd').get('composicao', None)
            if care:
                cares = care.split('<br>')
                care = list(filter(None, cares))
            return care

        def product_url():
            return response.urljoin(puket_skus["product_url"])

        def product_gender():
            return puket_skus.get('udasProd').get('google_gender', None)

        def product_brand():
            return puket_skus.get('udasProd').get('marca', None)

        def product_language():
            return response.css('html::attr(lang)').extract_first()

        def product_name():
            return response.css('.infoProduct .nameProduct::text').extract_first()

        def product_price():
            return response.css('.bestPrice .val::attr(content)').extract_first()

        def product_currency():
            return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()

        def product_categories():
            return response.css('.product-breadcrumb a::text').extract()[1:]

        def product_image_urls():
            return response.css('.list-thumbs a::attr(href)').extract()

        garment['retailer_sku'] = puket_skus['productId']
        garment['care'] = product_care()
        garment['trail'] = product_trail()
        garment['skus'] = product_skus()
        garment['url'] = product_url()
        garment['gender'] = product_gender()
        garment['brand'] = product_brand()
        garment['lang'] = product_language()
        garment['name'] = product_name()
        garment['price'] = product_price()
        garment['currency'] = product_currency()
        garment['category'] = product_categories()
        garment['image_urls'] = product_image_urls()
        return garment
