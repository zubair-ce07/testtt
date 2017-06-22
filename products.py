import scrapy
import json
import time


class QuotesSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://www.alexachung.com/uk/pointy-boots-black-76',
    ]

    def get_skus(self, response):
        item_details = {}
        try:
            _, item_details, _ = response.css('.fieldset script::text').extract()
        except ValueError:
            pass
        if item_details:
            item_details = json.loads(item_details)['[data-role=swatch-options]']['Magento_Swatches/js/swatch-renderer']
            item_product_ids = item_details['jsonConfig']['index']
            product_labels = item_details['jsonSwatchConfig']
            price = self.get_price(response)
            for product_key, product_details in item_product_ids.iteritems():
                item_product_ids[product_key].update({'size':
                                                        product_labels[next(iter(product_labels.keys()))][next(iter(
                                                        product_details.values()))]['value']})
                item_product_ids[product_key].update(price)
                item_product_ids[product_key].update({'color': 'blue'})
                item_product_ids[product_key].update({'currency': 'GBP'})
                return {'skus': item_product_ids}
        return {'skus': {}}

    def get_retailer_sku(self, response):
        product_id = response.css('.price-box.price-final_price')
        return {'retailer_sku': product_id.css('::attr(data-product-id)').extract_first()}

    def get_price(self, response):
        return {'price': response.css('.price-wrapper .price::text').extract_first()}

    def get_url(self, response):
        return {'url': response.url}

    def get_name(self, response):
        return {'name': response.css('.page-title::text').extract_first()}

    def get_description(self, response):
        description = response.css('.value')
        return {'description': description.css('p::text').extract()}

    def get_image_urls(self, response):
        images = response.css('.MagicZoom::attr(href)').extract()
        return {'image_urls': images}

    def construct_json(self, response):
        result_set = {}
        result_set.update(self.get_description(response))
        result_set.update(self.get_image_urls(response))
        result_set.update(self.get_retailer_sku(response))
        result_set.update(self.get_name(response))
        result_set.update(self.get_url(response))
        result_set.update(self.get_skus(response))
        result_set.update({'gender': 'female'})
        result_set.update({'brand': 'Alexa Chung'})
        result_set.update({'date': time.strftime("%H:%M:%S")})
        return result_set

    def parse(self, response):
        for next_item in response.css('.product.photo.product-item-photo::attr(href)').extract():
            yield response.follow(next_item, callback=self.parse)
        for next_category in response.css('.item.product.product-item'):
            yield response.follow(next_category, callback=self.parse)
        yield self.construct_json(response)

