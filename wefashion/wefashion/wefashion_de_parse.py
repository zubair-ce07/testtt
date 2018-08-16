from scrapy import Spider, Request

from wefashion.items import WefashionItem


class ProductParser(Spider):
    name = 'wefashion-de-parser'
    brand = "WE"
    visited_products = set()
    gender_map = {
        "herren": "men",
        "damen": "women",
        "jungen": "boys",
        "mädchen": "girls"
    }

    def parse(self, response):
        if self.if_product_exists(response):
            return

        item = WefashionItem()
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['trail'] = self.extract_trails(response)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['brand'] = self.brand
        item['url'] = response.url
        item['image_urls'] = self.extract_image_urls(response)
        item['name'] = self.extract_product_name(response)
        item['description'] = self.extract_product_description(response)
        item['care'] = self.extract_product_care(response)
        item['price'] = self.extract_price(response)
        item['currency'] = self.extract_currency(response)
        item['skus'] = self.extract_skus(response)
        item['requests'] = self.create_requests(response)
        return self.parse_requests(item)

    def parse_requests(self, item):
        if not item['requests']:
            del item['requests']
            return item

        request = item['requests'].pop()
        request.meta['item'] = item
        yield request

    def parse_product(self, response):
        item = response.meta['item']
        item['image_urls'].extend(self.extract_image_urls(response))
        item['skus'].update(self.extract_skus(response))
        return self.parse_requests(item)

    def create_requests(self, response):
        color_urls = self.extract_color_urls(response)
        return [Request(url, callback=self.parse_product) for url in color_urls]

    def if_product_exists(self, response):
        product_available = self.product_reference(response)
        retailer_sku = self.extract_retailer_sku(response)

        if not product_available or retailer_sku in self.visited_products:
            return True

        self.visited_products.add(retailer_sku)
        return False

    def extract_color_urls(self, response):
        color_id = self.extract_color_id(response)
        color_css = f".color :not(.unselectable) :not([data-value='{color_id}'])::attr(href)"
        return response.css(color_css).extract()

    def product_reference(self, response):
        return response.css('.pdp-main::attr(data-product-id)').extract_first()

    def extract_retailer_sku(self, response):
        return self.product_reference(response).split('_')[0]

    def extract_gender(self, response):
        gender_css = "meta[itemprop='name']::attr(content)"
        gender = response.css(gender_css).extract_first().split('-')[0]
        return self.gender_map.get(gender.lower())

    def extract_trails(self, response):
        return response.meta.get('trail')

    def extract_product_name(self, response):
        return response.css(".product-name ::text").extract_first().strip()

    def extract_product_description(self, response):
        description_css = "[itemprop='description'] div:not(:last-child) ::text"
        description = response.css(description_css).extract()
        return [text for text in description if text.strip()]

    def extract_product_care(self, response):
        care_css = "[itemprop='description'] div:last-child ::text"
        care = response.css(care_css).extract()
        return [text for text in care if text.strip()]

    def extract_price(self, response):
        price_css = "[itemprop='price']::attr(content)"
        return response.css(price_css).extract_first()

    def extract_currency(self, response):
        currecy_css = "[itemprop='priceCurrency']::attr(content)"
        return response.css(currecy_css).extract_first()

    def extract_color_id(self, response):
        return self.product_reference(response).split('_')[1]

    def extract_color(self, response):
        color_id = self.extract_color_id(response)
        color_id_css = f".color [data-value='{color_id}']::text"
        return response.css(color_id_css).extract_first(default='').strip()

    def extract_category(self, response):
        categories = response.css(".breadcrumb li ::text").extract()
        return [category for category in categories if category.strip()]

    def extract_image_urls(self, response):
        return response.css('::attr(data-image-replacement)').extract()

    def extract_sku_model(self, response):
        return response.css('::attr(data-value)').extract_first()

    def out_of_stock(self, response):
        return 'unselectable' in response.css('::attr(class)').extract_first()

    def extract_skus(self, response):
        color_id = self.extract_color_id(response)
        sku_info = {
            'color': self.extract_color(response),
            'currency': self.extract_currency(response),
            'price': self.extract_price(response)
        }

        skus = {}
        for size in response.css('.size li'):
            sku = sku_info.copy()
            sku['size'] = size.css('::attr(title)').extract_first()
            out_of_stock = self.out_of_stock(size)

            if out_of_stock:
                sku['out_of_stock'] = out_of_stock

            skus[f"{color_id}_{self.extract_sku_model(size)}"] = sku
        return skus
