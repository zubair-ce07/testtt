import json

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean
from ..parsers.jsparser import JSParser


class Mixin:
    retailer = "outdoorvoices-us"
    market = "US"
    allowed_domains = ["outdoorvoices.com"]
    start_urls = ["https://www.outdoorvoices.com/"]


class OutdoorVoicesParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + "-parse"

    def parse(self, response):
        product = JSParser(response.xpath('//script[contains(text(),"shopify_product_data")]/text()').extract_first())[
            "shopify_product_data"]
        sku_id = self.product_id(product)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate(garment, response)
        garment['name'] = self.product_name(response)
        garment['description'] = self.product_description(response)
        garment['brand'] = self.product_brand(response)
        garment['category'] = self.product_category(response)
        garment['image_urls'] = self.image_urls(product)
        garment['skus'] = self.skus(response, product)
        garment['merch_info'] = self.merch_info(response)
        garment['meta'] = {
            'requests_queue': self.description_request(response)
        }
        return self.next_request_or_garment(garment)

    def product_id(self, product):
        return product["id"]

    def product_name(self, response):
        return response.css('.product-hero__title ::text').extract_first()

    def product_category(self, response):
        return response.css('script.analytics::text').re('category":"([\w+\s?]+)')

    def product_brand(self, response):
        return "Outdoor Voices"

    def product_description(self, response):
        return clean(response.css('meta[property="og:description"]::attr(content)'))

    def product_care(self, raw_description):
        return list(
            set([(raw_care if self.care_criteria_simplified(raw_care) else None) for raw_care in raw_description]))

    def merch_info(self, response):
        name = self.product_name(response)
        return ["Limited Edition"] if "limited edition" in name.lower() else []

    def image_urls(self, product):
        sku_to_show = self.sku_to_show(product)
        images = []
        for image in product["images"]:
            if any(sku_id.split('-')[2] in image["src"] and "facebook" not in image["src"] for sku_id in sku_to_show):
                images.append(image["src"])
        return images

    def sku_to_show(self, product):
        sku_to_hide = product["metafields_admin"]["skus_to_hide"].split() if "skus_to_hide" in product else []
        return [sku["sku"] if sku["sku"] not in sku_to_hide else None for sku in product["variants"]]

    def skus(self, response, product):
        sku_to_show = self.sku_to_show(product)
        currency = response.css('meta[property="og:price:currency"]::attr(content)').extract_first()
        skus = {}
        for raw_sku in product["variants"]:
            if any(raw_sku["sku"] is sku_id for sku_id in sku_to_show):
                sku = self.product_pricing_common_new(response,
                                                      money_strs=[raw_sku['price'], currency,
                                                                  raw_sku['compare_at_price']],
                                                      is_cents=True)
                sku['colour'] = raw_sku['option1']
                sku['size'] = self.one_size if raw_sku['option2'] == 'OS' else raw_sku['option2']
                if not raw_sku['available']:
                    sku['out_of_stock'] = True
                sku_id = f'{sku["colour"]}_{sku["size"]}'
                skus[sku_id] = sku
        return self.filter_sku(skus)

    def filter_sku(self, skus):
        colours = list(set([sku['colour'] for key, sku in skus.items()]))
        colour_count = {colour: 0 for colour in colours}
        out_of_stock_count = colour_count.copy()
        for key, sku in skus.items():
            out_of_stock_count[sku['colour']] += 1 if 'out_of_stock' in sku else 0
            colour_count[sku['colour']] += 1
        sku_to_del = []
        for sku_id, sku in skus.items():
            if out_of_stock_count[sku['colour']] == colour_count[sku['colour']]:
                sku_to_del.append(sku_id)
        for sku_id in sku_to_del:
            del skus[sku_id]
        return skus

    def description_request(self, response):
        resource_id = response.css('script#__st::text').re('rid\":(\d+)')[0]
        url = f'https://mainframe.outdoorvoices.com/api/v2/product/{resource_id}/'
        return [Request(url=url, callback=self.parse_description)]

    def parse_description(self, response):
        garment = response.meta['garment']
        raw_description = self.product_raw_description(response)
        garment['care'] = clean(self.product_care(raw_description))
        garment['description'] = clean(self.product_updated_description(garment['description'] + raw_description))
        return self.next_request_or_garment(garment)

    def product_updated_description(self, raw_descriptions):
        description = []
        for raw_description in raw_descriptions:
            description += [description for description in raw_description.split('.')]
        return list(set(description))

    def product_raw_description(self, response):
        care, description = [], []
        raw_cares_html = set([raw_content["body"] for raw_content in json.loads(response.text)["copy"]])
        for raw_care_html in raw_cares_html:
            raw_cares = self.text_from_html(raw_care_html)
            for raw_care in raw_cares:
                description.append(raw_care)
        return description


class OutdoorVoicesCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = OutdoorVoicesParseSpider()

    listings_w_css = ['#women-dropdown']
    listings_m_css = ['#men-dropdown']

    products_css = ['.collection-variant__title-wrap']

    deny = ['gift-certificate']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_w_css, deny=deny), callback='parse_and_add_women'),
        Rule(LinkExtractor(restrict_css=listings_m_css, deny=deny), callback='parse_and_add_men'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse(self, response):
        for request in super(OutdoorVoicesCrawlSpider, self).parse(response):
            yield request
        resource_id = response.css('script#__st::text').re('rid\":(\d+)')[0]
        url = f'https://mainframe.outdoorvoices.com/api/v2/collection/{resource_id}/'
        response.meta['trail'] = self.add_trail(response)
        yield Request(url=url, meta=response.meta.copy(), callback=self.parse_categories)

    def parse_categories(self, response):
        for product in json.loads(response.text)["product_bundles"]:
            if product["swatches"]:
                url = product["swatches"][0]["shopify_path"]
                yield Request(url=url, meta=response.meta.copy(), callback=self.parse_spider.parse)

