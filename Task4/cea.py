import json

import requests
from scrapy import Spider, Request

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

    query_string = 'PS=48&cc=1&sm=0&sl=267cfeec-2b17-4122-9f04-c7abf8e5a82d'
    start_urls = [f'https://www.cea.com.br/buscapagina?ft=masculino&{query_string}&PageNumber=1'
                  , f'https://www.cea.com.br/buscapagina?ft=feminina&{query_string}&PageNumber=1'
                  , f'https://www.cea.com.br/buscapagina?ft=infantil&{query_string}&PageNumber=1'
                  , f'https://www.cea.com.br/buscapagina?ft=celulares&{query_string}&PageNumber=1'
                  , f'https://www.cea.com.br/buscapagina?ft=tablets&{query_string}&PageNumber=1'
                  , f'https://www.cea.com.br/buscapagina?ft=acessorios&{query_string}&PageNumber=1']

    def parse(self, response):
        item_links = response.css('.product-actions_details a::attr(href)').extract()
        for item_link in item_links:
            yield Request(item_link, callback=self.parse_item)

        url = response.url.split('=')
        next_page_url = f"{'='.join(url[:-1])}={int(url[-1])+1}"
        if item_links:
            yield Request(next_page_url)

    def parse_item(self, response):
        item = ProductItem()
        item['name'] = response.css('.productName::text').extract_first()
        item['retailer_sku'] = response.css('#___rc-p-id::attr(value)').extract_first()
        item['brand'] = response.css('td.Marca::text').extract_first()
        item['url'] = response.url
        item['category'] = self.get_category(item['retailer_sku'])
        item['price'] = self.get_price(response)
        item['gender'] = self.get_gender(response.url, item['name'])
        item['image_urls'] = self.get_image_urls(item['retailer_sku'])
        item['description'] = self.get_description(item['retailer_sku'])
        item['skus'] = self.get_skus(response)

        yield item

    def get_gender(self, url, item_name):
        if 'masculino' in url or 'masculino'in item_name:
            return 'Men'

        if 'feminina' in url or 'feminina'in item_name:
            return 'Women'

        return 'Unisex'

    def get_price(self, response):
        raw_price = response.css('#___rc-p-dv-id::attr(value)').extract_first()
        return float(raw_price.replace(',', '')) * 100

    def get_image_urls(self, item_id):
        image_ids = self.get_item_data(item_id)
        image_urls = [f"https://cea.vteximg.com.br/arquivos/ids/{image_id['imageId']}"
                      for image_id in image_ids['items'][0]['images']]
        return image_urls

    def get_item_data(self, id):
        uri = f"https://www.cea.com.br/api/catalog_system/pub/products/search?fq=productId:{id}"
        response = requests.get(uri)
        return json.loads(response.text)[0]

    def get_category(self, item_id):
        item_data = self.get_item_data(item_id)
        return item_data['categories']

    def get_description(self, item_id):
        item_data = self.get_item_data(item_id)
        return item_data['description']

    def get_skus(self, response):
        data = json.loads(response.css('script::text').re(r'var skuJson_0 = (.+]});')[0])
        filtered_skus = []
        for sku_json in data.get('skus'):
            filtered_skus.append({
                "colour": sku_json.get("dimensions").get("Cor"),
                "price": sku_json.get("bestPrice"),
                "Currency": "Brazilian real",
                "size": sku_json.get("dimensions").get("Volume", sku_json.get("Tamanho")),
                "out_of_stock": not sku_json.get("available"),
                "sku_id": sku_json.get("sku")
            })

        return filtered_skus
