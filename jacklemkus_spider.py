import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from jacklemkus.items import Product


class JacklemkusSpider(CrawlSpider):
    name = 'jacklemkus'
    currency = 'RAND'
    start_urls = ['https://www.jacklemkus.com/']
    allowed_domains = ['jacklemkus.com']

    listing_css = ['#nav .level0 > .menu-link', '.pagination .next']
    product_css = '.row .product-image'
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny='how-to-order'), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
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
        prod_name_css = '.product-essential .product-name h1::text'
        return response.css(prod_name_css).extract_first()

    def get_description(self, response):
        desc_css = '#description-tab .std::text'
        return list(map(str.strip, response.css(desc_css).extract()))

    def get_retailer_sku(self, response):
        prod_sku_css = '.prod-sku .sku::text'
        return response.css(prod_sku_css).extract_first()

    def get_image_urls(self, response):
        image_urls_css = '.product-essential .product-image a::attr(href)'
        return response.css(image_urls_css).extract()

    def get_gender(self, response):
        gender_css = '#product-attribute-specs-table tr:contains(Gender) .data::text'
        return response.css(gender_css).extract_first()

    def get_brand(self, response):
        brand_css = '#product-attribute-specs-table tr:contains(Brand) .data::text'
        return response.css(brand_css).extract_first()

    def get_product_url(self, response):
        return response.url

    def get_categories(self, response):
        category_css = ['.breadcrumbs li[itemprop="itemListElement"]:not(.home) a::text',
                        '#product-attribute-specs-table tr:contains({}) .data::text']
        categories = response.css(category_css[0]).extract()
        categories.append(response.css(category_css[1].format('DEPARTMENT')).extract_first())
        categories.append(response.css(category_css[1].format('Type')).extract_first())
        return list(filter(None, categories))

    def get_price(self, response):
        price_css = '.product-essential span.price::text'
        return response.css(price_css).extract_first()

    def get_skus(self, response):
        sku_css = '.product-data-mine::attr(data-lookup)'
        product_sel = response.css(sku_css)

        if not product_sel:
            return []

        product_details = json.loads(product_sel.extract_first().replace("\'", "\""))
        price = self.get_price(response)

        product_skus = []
        for raw_sku in product_details.values():
            sku = {"size": raw_sku.get("size"),
                   "sku_id": "{}_{}".format(raw_sku.get("id"),
                                            raw_sku.get("size").replace(" ", '_'))}

            if price[0] is 'R':
                sku["price"] = float(price[1:].replace(",", ""))
                sku["currency"] = JacklemkusSpider.currency

            if not raw_sku.get("stock_status"):
                sku["out_of_stock"] = True

            product_skus.append(sku)

        return product_skus
