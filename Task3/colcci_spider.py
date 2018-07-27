import json

from scrapy.spiders import Spider, Request

from Task3.items import ProductItem


class ColcciProductDetails(Spider):
    name = "Colcci"

    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 0.25,
        'ITEM_PIPELINES': {
            'Task3.pipelines.DuplicatesRemovalPipeline': 100,
        },
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output/productsdetail.json',
        'FEED_EXPORT_ENCODING': "utf-8",
    }

    start_urls = ['https://www.colcci.com.br/masculino-novo1/page/1'
                  , 'https://www.colcci.com.br/feminino-novo1/page/1'
                  , 'https://www.colcci.com.br/fitness/page/1'
                  , 'https://www.colcci.com.br/acessorios/page/1']

    def parse(self, response):

        yield Request(response.url, callback=self.parse_products, dont_filter=True)
        load_more = response.css('#loadMoreBtn').extract()
        if load_more:
            url = response.url.strip("/").split('/')
            next_page_url = f"{'/'.join(url[:-1])}/{int(url[-1])+1}"
            yield Request(next_page_url, callback=self.parse)

    def parse_products(self, response):
        item_links = response.css('[itemprop="name"] a::attr(href)').extract()
        for item_link in item_links:
            yield Request(item_link, callback=self.parse_item)

    def parse_item(self, response):
        selector = response.css(".descriptioncolContent")
        item = ProductItem()

        item['retailer_sku'] = self.get_retailer_sku(selector)
        item['name'] = self.get_item_name(selector)
        item['brand'] = 'Colcci'
        item['url'] = response.url
        item['category'] = self.get_category(item['name'])
        item['price'] = self.get_price(selector)
        item['description'] = self.get_description(selector)
        item['gender'] = self.get_gender(response)
        item['image_urls'] = self.get_image_urls(response)
        item['skus'] = self.get_skus(response)

        yield item

    def get_item_name(self, selector):
        return selector.css('[itemprop="name"]::text').extract_first()

    def get_retailer_sku(self, selector):
        return selector.css('[name="add_to_cart"]::attr(value)').extract_first()

    def get_category(self, item_name):
        return item_name.split(" ")[0]

    def get_price(self, selector):
        raw_price = selector.css('[itemprop="price"]::text').re_first('[\d+,]+')
        return float(raw_price.replace(',', ''))*100

    def get_image_urls(self, response):
        raw_image_urls = response.css(".cloud-zoom-gallery::attr(href)").extract()
        return [f"http:{url}" for url in raw_image_urls]

    def get_description(self, selector):
        raw_description = selector.css('#whatItIs *::text').extract()
        descriptions = [description.strip() for description in raw_description]
        return ''.join(descriptions)

    def get_gender(self, response):
        item_name = response.css('[itemprop="name"]::text').extract_first()

        if 'Unissex' in item_name:
            return 'Unisex'
        if 'masculino' in response.url:
            return 'Men'

        return 'Women'

    def get_skus(self, response):
        sku_jsons = json.loads(response.css("head script::text").re_first(r'.+LS.variants = (.+);'))
        skus = []
        for sku_json in sku_jsons:
            skus.append({
                "colour": sku_json.get("option0"),
                "price": sku_json.get("price_short"),
                "currency": "BRL",
                "size": sku_json.get("option1"),
                "previous_price": sku_json.get("compare_at_price_short"),
                "out_of_stock": not sku_json.get("available"),
                "sku_id": sku_json.get("sku")
            })

        return skus
