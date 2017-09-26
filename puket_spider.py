import re
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PuketSpider(CrawlSpider):

    name = "puket"
    allowed_domains = ['puket.com.br']
    start_urls = ['http://www.puket.com.br/']
    rules = (
        Rule(LinkExtractor(restrict_css=('#topMenu a',)), follow=True),
        Rule(LinkExtractor(restrict_css=('.shelf-category-list a',)), follow=True),
        Rule(LinkExtractor(restrict_css=('a.next',)), follow=True),
        Rule(LinkExtractor(restrict_css=('.box-product a.shelf-url',)), callback='parse_product'),
    )

    def parse_product(self, response):

        garment = {}

        def puket_skus():
            puket_skus_response = response.css('script[xml\:space="preserve"]::text').extract_first()
            puket_skus_json = re.search('(skuJson = )(.*\n)*', puket_skus_response).group(0)
            puket_skus_json = puket_skus_json.split('skuJson = ')[1].rsplit(';', 1)[0]
            puket_skus_ = json.loads(puket_skus_json)
            return puket_skus_

        puket_sku = puket_skus()

        def extract_with_css(selector):
            return response.css(selector).extract_first()

        def extract_all_with_css(selector):
            return response.css(selector).extract()

        def extract_trail(selector):
            trail = []
            visited_urls = extract_all_with_css(selector)
            for url in visited_urls:
                trail.append(response.urljoin(url))
            return trail

        def extract_care():
            care = puket_sku.get('udasProd').get('composicao', None)
            if care:
                care = care.split('<br>')
            return care

        def garment_skus():
            skus = []
            for sku in puket_sku["skus"]:
                skus.append({
                    'sku_id': sku['sku'],
                    'price': sku['bestPrice'],
                    'previous_prices': sku['listPrice'],
                    'currency': sku['currency'],
                    'colour': sku['udas']['COR'],
                    'size': sku['udas']['TAMANHO']
                })
            return skus

        garment['care'] = extract_care()
        garment['trail'] = extract_trail('.product-breadcrumb a::attr(href)')
        garment['skus'] = garment_skus()
        garment['url'] = response.urljoin(puket_sku["product_url"])
        garment['gender'] = puket_sku.get('udasProd').get('google_gender', None)
        garment['retailer_sku'] = puket_sku['productId']
        garment['brand'] = puket_sku.get('udasProd').get('marca', None)
        garment['lang'] = extract_with_css('html::attr(lang)')
        garment['name'] = extract_with_css('.infoProduct .nameProduct::text')
        garment['price'] = extract_with_css('.bestPrice .val::attr(content)')
        garment['currency'] = extract_with_css('[itemprop="priceCurrency"]::attr(content)')
        garment['category'] = extract_all_with_css('.product-breadcrumb a::text')[1:]
        garment['image_urls'] = extract_all_with_css('.list-thumbs a::attr(href)')
        return garment
