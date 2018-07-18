import json
from urllib.parse import urlparse

from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from jacklemkus.items import ProductItem


class ProductsSpider(CrawlSpider):
    name = 'jacklemkus'
    start_urls = ['https://www.jacklemkus.com']
    rules = (
        Rule(LinkExtractor(restrict_css='#nav li.level0>a', deny='how-to-order')),
        Rule(LinkExtractor(restrict_css='ol.row a.product-image'), 'parse_product'),
        Rule(LinkExtractor(restrict_css='ol.pagination.left a.next')),

    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse_product(self, response):
        xpath_query = "//body//div[@class='row']" \
                      "//tbody//th[contains(.,'{}')]/following-sibling::td/text()"
        base_url = urlparse(response.request.headers.get('Referer', 'None').decode("utf-8"))

        product_loader = ItemLoader(item=ProductItem(), response=response)
        product_loader.add_css('retailer_sku', 'div.product-essential span.sku::text')

        product_loader.add_xpath('gender', xpath_query.format('Gender'))

        product_loader.add_css('image_urls', 'div.product-essential p.product-image a::attr(href)')

        product_loader.add_css('description', '#description-tab div.std::text')

        product_loader.add_xpath('category', xpath_query.format('DEPARTMENT'))
        product_loader.add_xpath('category', xpath_query.format('Type'))
        product_loader.add_value('category', base_url.path[1:])

        product_loader.add_value('url', response.url)

        product_loader.add_css('name', 'div.product-essential div.product-name h1::text')

        product_loader.add_xpath('brand', xpath_query.format('Brand'))

        product_loader.add_value('skus', self.get_list_of_skus(response))
        return product_loader.load_item()

    @staticmethod
    def get_list_of_skus(response):
        lookup_mine = json.loads(response.css('div.product-data-mine::attr(data-lookup)')
                                 .extract_first().replace("\'", "\""))
        list_of_sku = []
        for item in lookup_mine.values():
            product_sku = {}
            price = response.css('div.product-essential span.price::text').extract_first()
            if price[0] is 'R':
                product_sku["price"] = float(price[1:].replace(",", ""))
                product_sku["currency"] = 'RAND'
            product_sku["size"] = item.get("size")
            product_sku["sku_id"] = "{}_{}".format(item.get("id"),
                                                   item.get("size").replace(" ", '_'))
            if not item.get("stock_status"):
                product_sku["out_of_stock"] = True
            list_of_sku.append(product_sku)
        return list_of_sku
