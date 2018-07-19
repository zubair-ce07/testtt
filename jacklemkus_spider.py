import json
from urllib.parse import urlparse

from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from jacklemkus.items import ProductItem


class ProductsSpider(CrawlSpider):
    name = 'jacklemkus'
    start_urls = ['https://www.jacklemkus.com/womens-apparel']
    rules = (
        Rule(LinkExtractor(restrict_css='#nav .level0 > .menu-link', deny='how-to-order')),
        Rule(LinkExtractor(restrict_css='.row .product-image'), 'parse_product'),
        Rule(LinkExtractor(restrict_css='pagination .next')),

    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse_product(self, response):
        base_url = urlparse(response.request.headers.get('Referer', 'None').decode("utf-8"))

        product_loader = ItemLoader(item=ProductItem(), response=response)

        product_loader.add_css('retailer_sku', '.prod-sku .sku::text')
        product_loader.add_css('image_urls', '.product-essential .product-image a::attr(href)')
        product_loader.add_css('description', '#description-tab .std::text')
        product_loader.add_css('name', '.product-essential .product-name h1::text')

        product_loader.add_value('gender', self.extract_attr(response, 'Gender'))
        product_loader.add_value('category', self.extract_attr(response, 'DEPARTMENT'))
        product_loader.add_value('category', self.extract_attr(response, 'Type'))
        product_loader.add_value('category', base_url.path[1:])
        product_loader.add_value('url', response.url)
        product_loader.add_value('brand', self.extract_attr(response, 'Brand'))
        product_loader.add_value('skus', self.extract_skus(response))

        return product_loader.load_item()

    @staticmethod
    def extract_attr(response, query):
        product_details = dict(
            zip(['Type' if row.endswith('Type') else row and
                 'Brand' if row.endswith('Brand') else row
                 for row in response.css('#more-info-tab .data-table .label::text').extract()],
                 response.css('#more-info-tab .data-table .data::text').extract())
            )
        return product_details.get(query)


    @staticmethod
    def extract_skus(response):
        product_skus = []
        product_sel = response.css('.product-data-mine::attr(data-lookup)')
        if any(product_sel):
            product_details = json.loads(product_sel.extract_first().replace("\'", "\""))
            for item in product_details.values():
                sku = {}
                price = response.css('.product-essential span.price::text').extract_first()
                if price[0] is 'R':
                    sku["price"] = float(price[1:].replace(",", ""))
                    sku["currency"] = 'RAND'
                sku["size"] = item.get("size")
                sku["sku_id"] = "{}_{}".format(item.get("id"), item.get("size").replace(" ", '_'))
                if not item.get("stock_status"):
                    sku["out_of_stock"] = True
                product_skus.append(sku)
        return product_skus
