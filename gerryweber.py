import scrapy
import json

from scrapy.spider import CrawlSpider, Rule
from gerrywebber.items import GerrywebberItem
from scrapy.linkextractor import LinkExtractor
import urllib.parse as urlparse
from urllib.parse import urlencode

class GerryScrapper(CrawlSpider):
    name = "Gerry_Weber"
    allowed_domains = ["house-of-gerryweber.de"]
    start_urls = ["http://www.house-of-gerryweber.de/Gerry-Weber/gerry,de,sc.html"]

    category_listing_x = ".//*[@id='cont_catmenu']/ul//li"

    rules = [Rule(LinkExtractor(restrict_xpaths=category_listing_x), ),
             Rule(LinkExtractor(restrict_xpaths=['//ul[@class="cat_products"]/li']),callback='parse_product_details')
            ]

    def parse_product_details(self, response):
        garment = GerrywebberItem()

        garment['spider_name'] = self.name
        garment['retailer'] = 'house_of_gerry_webber'
        garment['currency'] = 'EUR',
        garment['market'] = 'de'
        garment['brand'] = 'house of gerry webber'
        garment['name'] = self.product_name(response)
        garment['description'] = self.product_description(response)
        garment['selected_color'] = self.current_color(response)
        garment['retailer_sku'] = self.product_retailer_sku(response)
        garment['price'] = self.product_price(response)
        garment['url'] = response.url
        garment['url_original'] = response.url
        garment['image_urls'] = response.xpath(".//*[contains(@id, 'zoom')]/@href").extract()
        garment['gender'] = 'female'
        garment['skus'] = {}
        colors_map = self.get_color_map(response)

        yield scrapy.Request(url=self.skus_request_url(response),
                            meta={'garment': garment, 'color_map': colors_map},
                            callback=self.product_skus)

    def skus_request_url(self, response):
        product_ID = response.xpath("//*[contains(@id,'recommendations')]/@data-pid").extract()[0]
        url = "http://www.house-of-gerryweber.de/on/demandware.store/Sites-DE-Site/de/Product-GetVariants?pid=&format=json"
        params = {'pid': product_ID}
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        link = urlparse.urlunparse(url_parts)

        return link

    def product_skus(self, response):
        garment = response.meta['garment']
        color_map = response.meta['color_map']
        sku = {}
        product_variants = json.loads(response.text)
        variants = product_variants['variations']['variants']

        for items in variants:
            size = self.get_size(items)
            for key in color_map:
                if items['attributes']['color'] in color_map:
                    sku_details = {}
                    sku_details['size'] = size
                    sku_key = (color_map[key] + '_' + size)
                    sku_details['color'] = color_map[key]
                    sku_details['price'] = items['pricing']['sale']
                    sku_details['in_stock'] = items['avLevels']['IN_STOCK']
                    sku_details['previous_price'] = [items['pricing']['standard']]
                    sku[sku_key] = sku_details

        garment['skus'] = sku
        yield garment

    def get_size(self, variants):
        return variants['attributes'].get('size', 'one_size')

    def get_color_map(self, response):
        sel = response.css(".color a")
        color_map = {}
        for selector_path in sel:
            color_code = selector_path.xpath("./@data-value").extract()[0]
            title = selector_path.xpath("./@title").extract()[0]
            color_map[color_code] = title

        return color_map

    def product_name(self, response):
        return response.xpath("//*[contains(@class, 'productname')]//span[@itemprop='name']/text()").extract()[0]

    def product_description(self, response):
        return response.xpath("//*[@class='longdesc']//span/text()").extract()[0]

    def current_color(self, response):
        return response.xpath(".//*[contains(@class,'selected')]//a/@title").extract()[0]

    def product_retailer_sku(self, response):
        return response.xpath("//*[contains(@class, 'productid')]/span/text()").extract()[0]

    def product_price(self, response):
        return response.xpath("//*[contains(@class, 'productinfo')]//span[@itemprop='price']/text()").extract()[0]

