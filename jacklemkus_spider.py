import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from jacklemkus.items import Product


class JacklemkusSpider(CrawlSpider):
    name = 'jacklemkus'
    currency = 'RAND'
    start_urls = ['https://www.jacklemkus.com/']
    listing_css = ['#nav .level0 > .menu-link', '.pagination .next']
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny='how-to-order'), callback='parse'),
        Rule(LinkExtractor(restrict_css='.row .product-image'), callback='parse_product'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse_product(self, response):
        product_item = Product()

        product_item['retailer_sku'] = self.get_retailer_sku(response)
        product_item['image_urls'] = self.get_image_urls(response)
        product_item['description'] = self.get_description(response)
        product_item['name'] = self.get_product_name(response)

        product_item['gender'] = self.get_gender(response)
        product_item['category'] = self.get_categories(response)
        product_item['url'] = self.get_product_url(response)
        product_item['brand'] = self.get_brand(response)
        product_item['skus'] = self.get_skus(response)

        yield product_item

    def get_product_name(self, response):
        return response.css('.product-essential .product-name h1::text').extract_first()

    def get_description(self, response):
        return list(map(str.strip, response.css('#description-tab .std::text').extract()))

    def get_retailer_sku(self, response):
        return response.css('.prod-sku .sku::text').extract_first()

    def get_image_urls(self, response):
        return response.css('.product-essential .product-image a::attr(href)').extract()

    def get_gender(self, response):
        product_details = dict(
            zip([row for row in response.css('#more-info-tab .data-table .label::text').extract()],
                response.css('#more-info-tab .data-table .data::text').extract()))
        return product_details.get('Gender')

    def get_brand(self, response):
        product_details = dict(
            zip(['Brand' if row.endswith('Brand') else row
                 for row in response.css('#more-info-tab .data-table .label::text').extract()],
                response.css('#more-info-tab .data-table .data::text').extract()))

        return product_details.get('Brand')

    def get_product_url(self, response):
        return response.url

    def get_categories(self, response):
        product_details = dict(
            zip(['Type' if row.endswith('Type') else row and 'Brand' if row.endswith('Brand') else row
                 for row in response.css('#more-info-tab .data-table .label::text').extract()],
                response.css('#more-info-tab .data-table .data::text').extract()))

        category_css = '.breadcrumbs li[itemprop="itemListElement"]:not(.home) a::text'
        categories = response.css(category_css).extract()

        categories.append(product_details.get('DEPARTMENT'))
        categories.append(product_details.get('Type'))

        return list(filter(None, categories))

    def get_skus(self, response):
        product_skus = []

        product_sel = response.css('.product-data-mine::attr(data-lookup)')
        if not any(product_sel):
            return []
        product_details = json.loads(product_sel.extract_first().replace("\'", "\""))

        price = response.css('.product-essential span.price::text').extract_first()

        for item in product_details.values():
            sku = {}

            if price[0] is 'R':
                sku["price"] = float(price[1:].replace(",", ""))
                sku["currency"] = JacklemkusSpider.currency

            sku["size"] = item.get("size")

            sku["sku_id"] = "{}_{}".format(item.get("id"), item.get("size").replace(" ", '_'))

            if not item.get("stock_status"):
                sku["out_of_stock"] = True

            product_skus.append(sku)

        return product_skus
