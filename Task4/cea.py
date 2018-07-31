import json

from scrapy import Spider, Request
from w3lib import url

from Task4.items import ProductItem


class CeaSpider(Spider):
    name = 'cea'

    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 0.25,
        'ITEM_PIPELINES': {
            'Task4.pipelines.DuplicatesRemovalPipeline': 100,
        },
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output/productsdetail.json',
        'FEED_EXPORT_ENCODING': "utf-8",
    }

    base_url_t = 'https://www.cea.com.br/buscapagina?PS=48&cc=1&sm=0&sl=267cfeec-2b17-4122-9f04-c7abf8e5a82d&PageNumber=1&ft={}'

    def start_requests(self):
        urls = [CeaSpider.base_url_t.format(u) for u in
                  ('masculino', 'feminina', 'infantil', 'beauty', 'celulares', 'tablets', 'acessorios')]

        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        item_links = response.css('.product-actions_details a::attr(href)').extract()

        for item_link in item_links:
            yield Request(item_link, callback=self.parse_item)

        page_number = url.url_query_parameter(response.url, "PageNumber")
        next_page_url = url.add_or_replace_parameter(response.url, "PageNumber", int(page_number)+1)

        if item_links:
            yield Request(next_page_url)

    def parse_item(self, response):
        item = ProductItem()
        item['name'] = self.extract_item_name(response)
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['gender'] = self.extract_gender(response.url, item['name'])
        item['price'] = self.extract_price(response)
        item['brand'] = self.extract_brand(response)
        item['skus'] = self.extract_skus(response)
        item['url'] = response.url

        url = f"https://www.cea.com.br/api/catalog_system/pub/products/search?fq=productId:{item['retailer_sku']}"
        return Request(url, callback=self.parse_json_request, meta={'item': item})

    def parse_json_request(self, response):
        item_detail = json.loads(response.text)[0]
        item = response.meta["item"]
        item['category'] = self.extract_category(item_detail)
        item['image_urls'] = self.extract_image_urls(item_detail)
        item['description'] = self.extract_description(item_detail)
        return item

    def extract_item_name(self, response):
        return response.css('.productName::text').extract_first()

    def extract_retailer_sku(self, response):
        return response.css('#___rc-p-id::attr(value)').extract_first()

    def extract_brand(self, response):
        return response.css('td.Marca::text').extract_first()

    def extract_gender(self, url, item_name):
        gender_map = {
                        'Unissex': 'Unisex',
                        'masculino': 'Men',
                        'feminina': 'Women',
                        'Menina': 'Girl',
                        'Menino': 'Boy',
                        'Neutro': 'Kids'
        }

        for gender in gender_map.keys():
            if gender in item_name or gender in url:
                return gender_map[gender]

        return 'Unisex'

    def extract_price(self, response):
        raw_price = response.css('#___rc-p-dv-id::attr(value)').extract_first()
        return float(raw_price.replace(',', '')) * 100

    def extract_image_urls(self, item_detail):
        image_urls = [f"https://cea.vteximg.com.br/arquivos/ids/{image_id['imageId']}"
                      for image_id in item_detail['items'][0]['images']]
        return image_urls

    def extract_category(self, item_detail):
        return item_detail['categories']

    def extract_description(self, item_detail):
        return item_detail['description']

    def extract_skus(self, response):
        raw_skus = json.loads(response.css('script::text').re_first(r'var skuJson_0 = (.+]});'))
        skus = []

        for sku_json in raw_skus['skus']:
            sku = {
                "colour": sku_json.get("dimensions").get("Cor"),
                "price": sku_json.get("bestPrice"),
                "currency": "BRL",
                "size": sku_json.get("dimensions").get("Tamanho"),
                "sku_id": sku_json.get("sku")
            }

            if not sku_json.get("available"):
                sku["out_of_stock"] = True

            if sku_json.get("listPrice") > 0:
                sku["previous_prices"] = [sku_json.get("listPrice")]

            skus.append(sku)

        return skus
