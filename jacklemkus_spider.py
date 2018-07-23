import json
from urllib.parse import urlparse

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from jacklemkus.items import ProductItem


class ProductsSpider(CrawlSpider):
    name = 'jacklemkus'
    start_urls = ['https://www.jacklemkus.com/']
    rules = (
        Rule(LinkExtractor(restrict_css='#nav .level0 > .menu-link', deny='how-to-order')),
        Rule(LinkExtractor(restrict_css='.row .product-image'), 'parse_product'),
        Rule(LinkExtractor(restrict_css='.pagination .next')),

    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse_product(self, response):
        product_item = ProductItem()

        product_item['retailer_sku'] = self.get_retailer_sku(response)
        product_item['image_urls'] = self.get_image_urls(response)
        product_item['description'] = self.get_description(response)
        product_item['name'] = self.get_product_name(response)

        product_item['gender'] = self.extract_attr(response, 'Gender')
        product_item['category'] = self.extract_categories(response)
        product_item['url'] = response.url
        product_item['brand'] = self.extract_attr(response, 'Brand')
        product_item['skus'] = self.extract_skus(response)

        yield product_item

    @staticmethod
    def get_product_name(response):
        return response.css('.product-essential .product-name h1::text').extract_first()

    @staticmethod
    def get_description(response):
        return list(map(str.strip, response.css('#description-tab .std::text').extract()))

    @staticmethod
    def get_retailer_sku(response):
        return response.css('.prod-sku .sku::text').extract_first()

    @staticmethod
    def get_image_urls(response):
        return response.css('.product-essential .product-image a::attr(href)').extract()

    @staticmethod
    def extract_categories(response):
        categories = []
        base_url = urlparse(response.request.headers.get('Referer', 'None').decode("utf-8"))
        categories.append(ProductsSpider.extract_attr(response, 'DEPARTMENT'))
        categories.append(ProductsSpider.extract_attr(response, 'Type'))
        categories.append(base_url.path[1:])
        return list(filter(None, categories))

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
