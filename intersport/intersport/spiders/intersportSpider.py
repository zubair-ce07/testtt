import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from ..items import IntersportItem


class IntersportSpider(CrawlSpider):
    name = 'intersportSpider'
    start_urls = ['http://www.intersport.fr/']

    visited_items = set()

    LANG = 'fr'
    CURRENCY = 'EUR'
    BASE_URL = "http://www.intersport.fr"
    IMAGE_REQUEST_URL = ("http://media.intersport.fr/is/image/intersportfr/{retailer_id}_IS?req=set,json,UTF-8&"
                         "op_sharpen=1&$product_grey$&labelkey=label&id=177804284&handler=s7classics7sdkJSONResponse")
    IMAGE_BASE_URL = ("http://media.intersport.fr/is/image/{img_url}?op_sharpen=1&$product_grey$&layer=comp"
                      "&fit=constrain,1&wid=56&hei=56&fmt=jpg")

    rules = [Rule(LinkExtractor(restrict_css='.responsive-menu'), callback='parse', follow=True),
             Rule(LinkExtractor(restrict_css='.products-list'), callback='parse_item'), ]

    def parse(self, response):
        yield from super(IntersportSpider, self).parse(response)
        next_url_css = ".pagination-next a::attr(href)"
        next_url = response.css(next_url_css).extract_first()
        if next_url:
            yield response.follow(next_url, callback=self.parse)

    def parse_item(self, response):
        retailer_sku = self.item_retailer_sku(response)
        if self.is_visited(retailer_sku):
            return
        item = IntersportItem()
        product_name = self.item_product_name(response)
        item['lang'] = self.LANG
        item['brand'] = self.item_brand(response)
        item['care'] = self.item_care(response)
        item['category'] = self.item_category(response)
        item['description'] = self.item_description(response)
        item['name'] = product_name
        item['gender'] = self.item_gender(product_name)
        item['retailer_sku'] = retailer_sku
        item['url'] = response.url
        color_urls = response.css(".colors-slider .product-image a::attr(name)").extract()
        yield response.follow(self.BASE_URL + color_urls.pop(), callback=self.parse_item_skus,
                              meta={'item': item, 'color_urls': color_urls}, dont_filter=True)

    def parse_item_skus(self, response):
        item = response.meta['item']
        if 'skus' in item:
            item_skus = item['skus']
        else:
            item_skus = {}
        img_urls = response.meta.get('img_urls')
        if not img_urls:
            img_urls = []

        retailer_id = self.item_retailer_sku(response)
        item_skus.update(self.item_skus(response, retailer_id))
        img_urls.append(self.item_image_request_url(response, retailer_id))

        item['skus'] = item_skus
        color_urls = response.meta['color_urls']

        if not color_urls:
            yield response.follow(img_urls.pop(),
                                  callback=self.parse_item_image_urls,
                                  meta={'item': item, 'img_urls': img_urls})
        else:
            yield response.follow(self.BASE_URL + color_urls.pop(),
                                  callback=self.parse_item_skus,
                                  meta={'item': item, 'color_urls': color_urls,
                                        'img_urls': img_urls})

    def parse_item_image_urls(self, response):
        item = response.meta['item']
        img_urls = response.meta['img_urls']
        if 'image_urls' in item:
            image_urls = item['image_urls']
        else:
            image_urls = []
        item['image_urls'] = self.item_image_urls(response, image_urls)
        if not img_urls:
            yield item
        else:
            yield response.follow(img_urls.pop(), callback=self.parse_item_image_urls,
                                  meta={'item': item, 'img_urls': img_urls})

    def is_visited(self, retailer_sku):
        if retailer_sku in self.visited_items:
            return True
        self.visited_items.add(retailer_sku)
        return False

    def item_retailer_sku(self, response):
        item_id = response.css('.ref-produit::text').extract_first()
        if item_id:
            return item_id.split("Ref ")[1]

    def item_product_name(self, response):
        return response.css("a[class=link] h1::text").extract_first()

    def item_care(self, response):
        item_care = response.css(".body-panel .small-12::text").extract()
        return [c.strip() for c in item_care if c.strip()]

    def item_category(self, response):
        return response.css(".breadcrumbs a::text").extract()[1:-1]

    def item_description(self, response):
        description = response.css(".body-panel p::text").extract()
        return [d.strip() for d in description if d.strip()]

    def item_gender(self, product_name):
        gender = 'unisex'
        gen_dict = {'femme': 'women', 'homme': 'men', 'enfant': 'unisex-kids',
                    'garcon': 'boy', 'fille': 'girl'}
        for key, values in gen_dict.items():
            if key in product_name.lower():
                gender = values
                break
        return gender

    def item_brand(self, response):
        return response.css("a[class=link] a::text").extract_first()

    def item_active_color(self, response):
        return response.css('.ref-produit::text').extract_first()[-3:]

    def item_old_price(self, response):
        old_price = "".join(response.css('.old-price ::text').extract()[:2])
        if old_price:
            return old_price.replace(old_price[2], "").strip()

    def item_new_price(self, response):
        new_price = "".join(response.css('.current-price ::text').extract()[:2])
        return new_price.replace(new_price[2], "").strip()

    def item_sizes(self, response):
        sizes = {}
        size_selector = response.css(".tailles-produit button")
        for selector in size_selector:
            status = 'available'
            size = selector.css("::text").extract_first().strip()
            if selector.css('button[disabled]'):
                status = 'unavailable'
            sizes[size] = status
        return sizes

    def item_skus(self, response, retailer_id):
        skus = {}
        colour = self.item_active_color(response)
        for size, status in self.item_sizes(response).items():
            temp_skus = {}
            temp_skus['size'] = size
            if status == 'available':
                temp_skus['colour'] = colour
                temp_skus['currency'] = self.CURRENCY
                temp_skus['current_price'] = self.item_new_price(response)
                temp_skus['old_price'] = self.item_old_price(response)
            temp_skus['status'] = status
            color_id = retailer_id.replace(" ", "") + size
            skus[color_id] = temp_skus
        return skus

    def item_image_request_url(self, response, retailer_id):
        return self.IMAGE_REQUEST_URL.format(retailer_id=retailer_id.replace(" ", "_"))

    def item_image_urls(self, response, image_urls):
        decoded_response = response.body.decode(response.encoding)
        response_json = eval(decoded_response[decoded_response.index('(') + 1:decoded_response.index('}},') + 2])
        for img_item in response_json.get('set').get('item'):
            if img_item:
                img_url = img_item.get('i').get('n')
                image_urls.append(self.IMAGE_BASE_URL.format(img_url=img_url))
        return image_urls
