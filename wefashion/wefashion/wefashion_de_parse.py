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
        item = WefashionItem()
        product_available = self.product_available(response)
        if not product_available or self.extract_retailer_sku(response) in self.visited_products:
            return

        retailer_sku = self.extract_retailer_sku(response)
        item['retailer_sku'] = retailer_sku
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
        color_urls = self.extract_product_urls(response)
        self.visited_products.add(retailer_sku)
        if color_urls:
            yield self.create_request(color_urls.pop(), meta={'item': item, 'urls': color_urls})

        return item

    def parse_product(self, response):
        item = response.meta['item']
        color_urls = response.meta['urls']

        image_urls = response.meta.get('image_urls', [])
        previous_skus = response.meta.get('skus', {})

        image_urls.append(self.extract_image_urls(response))
        previous_skus.update(self.extract_skus(response))

        if not color_urls:
            image_urls.append(item['image_urls'])
            item['image_urls'] = image_urls
            item['skus'].update(previous_skus)
            return item

        yield self.create_request(color_urls.pop(),
                                  meta={'item': item, 'urls': color_urls,
                                        'skus': previous_skus, 'image_urls': image_urls})

    def create_request(self, url, meta):
        return Request(url=url, callback=self.parse_product, meta=meta)

    def extract_product_urls(self, response):
        color_id = self.extract_color_id(response)
        return response.css(f".color :not(.unselectable)"
                            f" :not([data-value='{color_id}'])::attr(href)").extract()

    def product_available(self, response):
        return response.css('.pdp-main::attr(data-product-id)').extract_first()

    def extract_retailer_sku(self, response):
        return self.product_available(response).split('_')[0]

    def extract_gender(self, response):
        gender = response.css("meta[itemprop='name']::attr(content)").extract_first().split('-')[0]
        return self.gender_map.get(gender.lower())

    def extract_trails(self, response):
        return response.meta.get('trail')

    def extract_product_name(self, response):
        return response.css(".product-name ::text").extract_first().strip()

    def extract_product_description(self, response):
        description = response.css("[itemprop='description'] div:not(:last-child) ::text").extract()
        return list(filter(lambda text: text.strip(), description))

    def extract_product_care(self, response):
        care = response.css("[itemprop='description'] div:last-child ::text").extract()
        return list(filter(lambda text: text.strip(), care))

    def extract_price(self, response):
        return response.css("[itemprop='price']::attr(content)").extract_first()

    def extract_currency(self, response):
        return response.css("[itemprop='priceCurrency']::attr(content)").extract_first()

    def extract_color_id(self, response):
        return self.product_available(response).split('_')[1]

    def extract_color(self, response):
        color_id = self.extract_color_id(response)
        return response.css(f".color [data-value='{color_id}']::text").extract_first(default='').strip()

    def extract_category(self, response):
        categories = response.css(".breadcrumb li ::text").extract()
        return list(filter(lambda category: category.strip(), categories))

    def extract_image_urls(self, response):
        return response.css('::attr(data-image-replacement)').extract()

    def extract_sku_model(self, response):
        return response.css('::attr(data-value)').extract_first()

    def in_stock(self, response):
        if 'unselectable' in response.css('::attr(class)').extract_first():
            return True
        return False

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
            sku['out_of_stock'] = self.in_stock(size)
            skus[f"{color_id}_{self.extract_sku_model(size)}"] = sku
        return skus
