from scrapy import Spider

from wefashion.items import WefashionItem


class ProductParser(Spider):
    name = 'wefashion-de-parser'
    brand = "WE"
    gender_map = {
        "herren": "men",
        "damen": "women",
        "jungen": "boys",
        "mädchen": "girls"
    }

    def parse(self, response):
        item = WefashionItem()
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['trail'] = self.extract_trails(response)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['brand'] = self.brand
        item['url'] = response.url
        item['name'] = self.extract_product_name(response)
        item['description'] = self.extract_product_description(response)
        item['care'] = self.extract_product_care(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['skus'] = self.extract_skus(response)
        item['price'] = self.extract_price(response)
        item['currency'] = self.extract_currency(response)
        return item

    def extract_retailer_sku(self, response):
        return response.css('.pdp-main::attr(data-product-id)').extract_first()

    def extract_gender(self, response):
        gender = response.css("meta[itemprop='name']::attr(content)").extract_first().split('-')[0].lower()
        return self.gender_map.get(gender)

    def extract_trails(self, response):
        return response.meta.get('trail')

    def extract_product_name(self, response):
        return response.css(".product-name ::text").extract_first().strip()

    def extract_product_description(self, response):
        description = response.css("[itemprop='description']  ::text").extract()
        description = list(filter(lambda text: text.strip(), description))
        return description[:description.index('Waschanleitung')]

    def extract_product_care(self, response):
        description = response.css("[itemprop='description']  ::text").extract()
        description = list(filter(lambda text: text.strip(), description))
        return description[description.index('Waschanleitung'):]

    def extract_price(self, response):
        return response.css("meta[itemprop='price']::attr(content)").extract_first()

    def extract_currency(self, response):
        return response.css("[itemprop='priceCurrency']::attr(content)").extract_first()

    def extract_color(self, response):
        color_id = self.extract_retailer_sku(response).split('_')[1]
        return response.css(f".color [data-value='{color_id}']::text").extract_first(default='').strip()

    def extract_category(self, response):
        categories = response.css(".breadcrumb li ::text").extract()
        return list(filter(lambda category: category.strip(), categories))

    def extract_image_urls(self, response):
        return response.css('::attr(data-image-replacement)').extract()

    def extract_sku_sizes(self, response):
        sku_sizes = response.css('.size li ::attr(title)').extract()
        return sku_sizes

    def extract_sku_models(self, response):
        sku_models = response.css('.size li ::attr(data-value)').extract()
        return sku_models

    def extract_skus(self, response):
        sku_sizes = self.extract_sku_sizes(response)
        sku_models = self.extract_sku_models(response)
        sku_info = {
            'color': self.extract_color(response),
            'currency': self.extract_currency(response),
            'price': self.extract_price(response)
        }

        skus = {}
        for sku_model, size in zip(sku_models, sku_sizes):
            sku = sku_info.copy()
            sku['size'] = size
            skus[sku_model] = sku

        return skus
