import re
import time
import json
import scrapy

from itertools import product
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from woolrich_itemloaders.items import ProductLoader, SkuLoader, split_price

class ProductsSpider(CrawlSpider):
    name = "woolrich_itemloader"
    start_urls = ['https://www.woolrich.com/']
    attr_url = "https://www.woolrich.com/remote/v1/product-attributes/"
    rules = (
        Rule(LinkExtractor(restrict_css=["#primary > ul > li", ".pagination-item--next"])),
        Rule(LinkExtractor(restrict_css=".card-figure"), callback="parse_item")
    )

    def parse_item(self, response):
        product_loader = ProductLoader(response=response)
        product_loader.add_css("retailer_sku", ".parent-sku::text")
        product_loader.add_css("lang", "html::attr(lang)")
        product_loader.add_css("gender", ".breadcrumb-label::text")
        product_loader.add_css("category", ".breadcrumb-label::text")
        product_loader.add_value("url", response.url)
        product_loader.add_value("date", time.time())
        product_loader.add_css("market", ".navPages-item--location img::attr(alt)")
        product_loader.add_css("name", ".productView-title::text")
        product_loader.add_css("desc", "#details-content::text")
        product_loader.add_css("care", "ul#features-content li::text")
        product_loader.add_css("image_urls", "#zoom-modal img::attr(src)")
        product_loader.add_value("skus", {})
        product_loader.add_css("price", ".productView-details .price::text")
        product_loader.add_css("currency", ".productView-details .price::text")
        item = product_loader.load_item()

        sku_requests = self.get_sku_requests(response, item)
        if sku_requests:
            sku_request = sku_requests.pop()
            sku_request['metadata']['sku_requests'] = sku_requests
            yield scrapy.FormRequest(
                url = sku_request['url'],
                formdata = sku_request['formdata'],
                meta = sku_request['metadata'],
                callback = self.parse_skus
            )
    
    def parse_skus(self, response):
        obj = json.loads(response.text)
        if 'rrp_without_tax' in obj['data']['price']:
            previous_price = split_price(obj['data']['price']['rrp_without_tax']['formatted'])
        else:
            previous_price = None
        
        sku_loader = SkuLoader(response=response)
        sku_loader.add_value("price", obj['data']['price']['without_tax']['formatted'])
        sku_loader.add_value("currency", obj['data']['price']['without_tax']['formatted'])
        sku_loader.add_value("previous_price", previous_price)
        sku_loader.add_value("color", response.meta['color'])
        sku_loader.add_value("size", response.meta['size'])
        sku_loader.add_value("availability", obj['data']['instock'])
        sku = sku_loader.load_item()
        response.meta['item']['skus'].update({obj['data']['sku']: sku})
        
        if response.meta['sku_requests']:
            sku_request = response.meta['sku_requests'].pop()
            yield scrapy.FormRequest(
                url = sku_request['url'],
                formdata = sku_request['formdata'],
                meta = sku_request['metadata'],
                callback = self.parse_skus
            )
        else:
            yield response.meta['item']
        
    def get_sku_requests(self, response, item):
        color_attr_unformatted = response.css('.productView-details [data-swatch-id]::attr(data-swatch-id)').get()
        attr_for_size = response.css(".productView-details .product-size .form-radio::attr(name)").get()
        attr_for_color = f"attribute[{color_attr_unformatted}]"
        size_ids = response.css(".productView-options .product-size .form-radio::attr(value)").getall()
        color_ids = response.css(".productView-options [aria-checked]::attr(value)").getall()
        color_names = response.css(".productView-options [data-swatch-id]::attr(title)").getall()
        size_names = response.css(".productView-options .product-size .form-option span::text").getall()
        item_id = response.css(".jrb-product-view::attr(data-entity-id)").get()

        combinations = list(product(color_ids, size_ids))
        meta = {
                'color_attr': attr_for_color,
                'size_attr': attr_for_size,
                'item_id': item_id,
                'color': '',
                'size': '',
                'color_names': color_names,
                'size_names': size_names,
                'color_ids': color_ids,
                'size_ids': size_ids,
                'item': item,
                'sku_requests': []
        }
        requests = []
        for combination in combinations:
            color, size = combination
            meta['color'] = color_names[color_ids.index(color)]
            meta['size'] = size_names[size_ids.index(size)]
            sku_request = {
                'url': f"{self.attr_url}{meta['item_id']}",
                'formdata': {
                    'action': 'add',
                    meta['color_attr']: color,
                    meta['size_attr']: size,
                    'product_id': meta['item_id'],
                    'qty[]': '1'
                },
                'metadata': meta
            }
            requests.append(sku_request)
        return requests
