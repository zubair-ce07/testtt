import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Task3.items import ProductItem


class ColcciProductDetails(CrawlSpider):
    name = "Colcci"
    start_urls = ['https://www.colcci.com.br/']

    allowed_links = ('masculino-novo1', 'feminino-novo1', 'fitness', 'acessorios')
    rules = (Rule(LinkExtractor(allow=allowed_links, restrict_css=".with-subitems")),
             Rule(LinkExtractor(deny='page', restrict_css=".products-list"), callback='parse_page'),)

    def parse_page(self, response):
        selector = response.css(".descriptioncolContent")
        item = ProductItem()

        item['retailer_sku'] = selector.css('[name="add_to_cart"]::attr(value)').extract_first()
        item['name'] = selector.css('[itemprop="name"]::text').extract_first()
        item['brand'] = 'Colcci'
        item['url'] = response.url
        item['category'] = self.get_category(item['name'])
        item['price'] = self.get_price_in_cents(selector)
        item['description'] = self.get_description(selector)
        item['gender'] = self.get_gender_from_url(response)
        item['image_urls'] = self.get_image_urls(response)
        item['skus'] = self.get_required_skus(response)

        yield item

    def get_category(self, item_name):
        return item_name.split(" ")[0]

    def get_price_in_cents(self, selector):
        raw_price = selector.css('[itemprop="price"]::text').extract_first()
        return float(raw_price[2:].replace(',', '')) * 100

    def get_image_urls(self, response):
        raw_image_urls = response.css(".cloud-zoom-gallery::attr(href)").extract()
        return [f"http:{url}" for url in raw_image_urls]

    def get_description(self, selector):
        raw_description = selector.xpath('//*[@id="whatItIs"]//text()').extract()
        descriptions = [description.strip() for description in raw_description]
        return ''.join(descriptions)

    def get_gender_from_url(self, response):
        name_url_string = response.css('[itemprop="name"]::text').extract_first() + response.url
        if 'Unissex' in name_url_string:
            return 'Unisex'
        if 'masculino' in name_url_string:
            return 'boy'

        return 'girl'

    def get_required_skus(self, response):
        sku_jsonobjects = json.loads(response.css("head script::text").re_first(r'.+LS.variants = (.+);'))
        filtered_skus = []
        if sku_jsonobjects:
            for sku_jsonobject in sku_jsonobjects:
                filtered_skus.append({
                    "colour": sku_jsonobject.get("option0", None),
                    "price": sku_jsonobject.get("price_short", None),
                    "Currency": "Brazilian real",
                    "size": sku_jsonobject.get("option1", None),
                    "previous_price": sku_jsonobject.get("compare_at_price_short", None),
                    "out_of_stock": not sku_jsonobject.get("available", None),
                    "sku_id": sku_jsonobject.get("sku", None)
                })

            return filtered_skus

