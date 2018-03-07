import re
import json

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender


class MixinCA:
    retailer = "converse-ca"
    start_urls = ["https://www.converse.ca/"]
    allowed_domain = ["www.converse.ca"]
    market = "CA"


class ConverseParseSpider(BaseParseSpider):
    price_css = '.mob-price span ::text'

    brand_map = [
        'Converse',
        'Converse x Dr Woo',
        'Converse x NBA',
    ]

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment["image_urls"] = self.image_urls(response)
        garment["gender"] = self.product_gender(response)
        garment["skus"] = self.skus(response)

        return garment

    def product_id(self, response):
        return self.magento_product_id(response)

    def product_name(self, response):
        return clean(response.css('.product-name h1 ::text'))[0]

    def raw_description(self, response):
        desc_sel = response.css('.mob')
        return clean(desc_sel.css('.full-description p ::text,.benefits li ::text,.full-origins p ::text'))

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def product_category(self, response):
        return clean(response.css('::attr(data-category)'))[0].split('/')

    def product_gender(self, response):
        soup = [
            ' '.join(self.product_category(response)) + self.product_name(response),
            ' '.join([url for _, url in response.meta.get("trail", [])])
        ]
        return self.gender_lookup(soup[0]) or self.gender_lookup(soup[1]) or Gender.ADULTS.value

    def product_brand(self, response):
        name = self.product_name(response)
        brand = [brand for brand in self.brand_map if brand in name]
        return ''.join(brand) if brand else "converse"

    def image_urls(self, response):
        return clean(response.css('.gallery-image ::attr(src)'))[1:]

    def raw_colours(self, response):
        raw_colours = response.xpath('//script[contains(text(),"StyleIdOjc")]/text()').extract_first()
        if raw_colours:
            colours = re.findall('StyleIdOjc = (.+})', raw_colours)[-1]
            colours = json.loads(colours)
            return {key[0]: key[1] for key in colours.values()}

    def skus(self, response):
        skus = {}
        multiple_colours = self.raw_colours(response)
        one_colour = clean(response.css('.product-color-container ::text'))[0]
        spconfig = self.magento_product_data(response)
        raw_skus = self.magento_product_map(spconfig)
        common_sku = self.product_pricing_common_new(response)

        for sku_id, variants in raw_skus.items():
            size_label = []
            colour_label = []

            for variant in variants:
                sku = common_sku.copy()
                if variant["name"] == "Style":
                    colour_label.append(variant["label"])

                else:
                    size_label.append(variant["label"])
                sku["colour"] = multiple_colours.get(colour_label[0]) if colour_label else one_colour
                size = ''.join(size_label)
                sku["size"] = self.one_size if size == "One Size" else size
                skus[sku_id] = sku

        return skus


class ConverseCrawlSpider(BaseCrawlSpider):
    listing_css = [
        '.level2',
        'link[rel="next"]'
    ]
    product_css = '.product-name'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")
    )


class ConverseParseSpiderCA(MixinCA, ConverseParseSpider):
    name = MixinCA.retailer + "-parse"


class ConverseCrawlSpiderCN(MixinCA, ConverseCrawlSpider):
    name = MixinCA.retailer + "-crawl"
    parse_spider = ConverseParseSpiderCA()
