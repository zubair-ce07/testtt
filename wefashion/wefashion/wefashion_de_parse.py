from scrapy import Spider, Request

from wefashion.items import WefashionItem


class ProductParser(Spider):
    name = 'wefashion-de-parser'
    brand = "WE"
    visited_urls = set()
    gender_map = {
        "herren": "men",
        "damen": "women",
        "jungen": "boys",
        "mädchen": "girls"
    }

    def parse(self, response):
        item = WefashionItem()
        retailer_sku = self.extract_retailer_sku(response)
        if retailer_sku in self.visited_urls or None:
            return

        item['retailer_sku'] = retailer_sku.split('_')[0]
        item['trail'] = self.extract_trails(response)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['brand'] = self.brand
        item['url'] = response.url
        item['name'] = self.extract_product_name(response)
        item['description'] = self.extract_product_description(response)
        item['care'] = self.extract_product_care(response)
        item['price'] = self.extract_price(response)
        item['currency'] = self.extract_currency(response)
        total_items = len(self.extract_product_urls(response))
        color_urls = self.extract_product_urls(response)
        self.visited_urls.add(retailer_sku)

        if total_items > 0:
            yield self.create_request(color_urls.pop(), {'item': item, 'size': total_items,
                                                         'urls': color_urls})

    def parse_product(self, response):
        item = response.meta['item']
        total_items = response.meta['size']

        image_urls = response.meta.get('image_urls', [])
        previous_skus = response.meta.get('skus', {})

        image_urls.append(self.extract_image_urls(response))
        previous_skus.update(self.extract_skus(response))

        if total_items <= 1:
            item['image_urls'] = image_urls
            item['skus'] = previous_skus
            return item

        color_urls = response.meta['urls']
        yield self.create_request(color_urls.pop(),
                                  {'item': item, 'size': total_items - 1, 'urls': color_urls,
                                   'skus': previous_skus, 'image_urls': image_urls})

    def create_request(self, url, meta_info):
        return Request(url=url, callback=self.parse_product, meta=meta_info)

    def extract_product_urls(self, response):
        return response.css('.color :not(.unselectable) a::attr(href)').extract()

    def extract_retailer_sku(self, response):
        return response.css('.pdp-main::attr(data-product-id)').extract_first()

    def extract_gender(self, response):
        gender = response.css("meta[itemprop='name']::attr(content)").extract_first(default='').split('-')[0]
        return self.gender_map.get(gender.lower())

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

    def extract_color_id(self, response):
        return self.extract_retailer_sku(response).split('_')[1]

    def extract_color(self, response):
        color_id = self.extract_color_id(response)
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
        color_id = self.extract_color_id(response)
        sku_info = {
            'color': self.extract_color(response),
            'currency': self.extract_currency(response),
            'price': self.extract_price(response)
        }

        skus = {}
        for sku_model, size in zip(sku_models, sku_sizes):
            sku = sku_info.copy()
            sku['size'] = size
            skus[f"{color_id}_{sku_model}"] = sku

        return skus
