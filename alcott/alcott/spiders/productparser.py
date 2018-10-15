import re
import datetime

from alcott.items import Product


class ProductParser():
    name = 'alcot-parser'

    def parse(self, response):
        item = Product()

        item['retailer_sku'] = self.product_retailer_sku(response)
        item['trail'] = self.product_trail(response)
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['brand'] = 'Alcott'
        item['url'] = response.url
        item['date'] = str(datetime.date.today())
        item['market'] = 'EU'
        item['retailer'] = 'Alcott-EU'
        item['url_original'] = response.url
        item['name'] = self.product_name(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.product_image_urls(response)
        item['skus'] = self.product_skus(response)
        item['spider_name'] = self.name
        item['crawl_start_time'] = str(datetime.datetime.now().time())

        yield item

    def product_retailer_sku(self, response):
        css = '.sku::text'
        data = response.css(css).extract_first()
        retailer_sku = data.split(':')[-1]
        return retailer_sku

    def product_trail(self, response):
        css = '[property*=url]::attr(content)'
        return response.css(css).extract()

    def product_gender(self, response):
        css = '#widget_breadcrumb li:nth-child(2) a::text'
        category = response.css(css).extract_first()
        return str(category).strip()

    def product_category(self, response):
        css = '#widget_breadcrumb li:nth-last-child(2) a::text'
        category = response.css(css).extract_first()
        return str(category).strip()

    def product_name(self, response):
        css = '.main_header::text'
        return response.css(css).extract_first()

    def product_care(self, response):
        css = '#itemCareList span::text'
        data = response.css(css).extract()
        return [item.strip() for item in data]

    def product_image_urls(self, response):
        data = self.extract_data(response)
        return [self.extract_images(item['PhotoGallery']) for item in data]

    def product_skus(self, response):
        data = self.extract_data(response)
        items = [self.extract_attributes(item['Attributes']) for item in data]

        skus = {}
        for item in items:
            sku = {}
            sku['color'] = item[0]
            sku['size'] = item[1]
            sku['price'] = self.product_price(response)
            sku['currency'] = self.product_currency(response)
            unique_id = sku['color'] + "_" + sku['size']
            skus.update({unique_id: sku})
        return skus

    def extract_data(self, response):
        css = '[id*=entitledItem]::text'
        data = response.css(css).extract_first()
        data = re.sub('[\n\r\t]', '', data)
        data = eval(data)
        return data

    def extract_images(self, data):
        return [item['base'] for item in data]

    def extract_attributes(self, data):
        attributes = data.keys()
        attributes = [item.split('_|_')[-1] for item in attributes]
        return attributes

    def chunks(self, data, index):
        for i in range(0, len(data), index):
            yield data[i:i+index]

    def product_price(self, response):
        css = '[id*=ProductInfoPrice]::attr(value)'
        data = response.css(css).extract_first()
        price = data.split(';')[-1]
        price = re.sub('[.]', '', price)
        return price

    def product_currency(self, response):
        css = '[id*=ProductInfoPrice]::attr(value)'
        data = response.css(css).extract_first()
        currency = data.split(';')[0]
        currency = re.sub('&', '', currency)
        return currency
