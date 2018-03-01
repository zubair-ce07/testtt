from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class MixinCN:
    retailer = "converse-cn"
    start_urls = ["http://www.converse.com.cn/"]
    allowed_domain = ["www.converse.com.cn"]
    market = "CN"


class ConverseParseSpider(BaseParseSpider):
    price_css = '.product-price span ::text'
    spider_gender_map = [("女的", "women"), ('男的', "men"), ("男女", "men"), ("小童", "unisex-kids"),
                         ("小孩", "unisex-kids"), ("童", "unisex-kids")]

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.skus(response)
        garment["gender"] = self.product_gender(response)

        if not garment["skus"]:
            garment.update(self.product_pricing_common_new(response))
            garment["out_of_stock"] = True

        return garment

    def product_id(self, response):
        return clean(response.css('#skuCode ::attr(value)'))[0]

    def product_name(self, response):
        return clean(response.css('#product-name ::text'))[0]

    def image_urls(self, response):
        img_urls = clean(response.css('.product-thumb-list a ::attr(data-img)'))
        return [response.urljoin(img_url.replace('S', "L")) for img_url in img_urls]

    def product_description(self, response):
        raw_description = clean(response.css('.product-description li ::text'))
        return [rd for rd in raw_description if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        raw_description = clean(response.css('.product-description li ::text'))
        return [rd for rd in raw_description if self.care_criteria_simplified(rd)]

    def product_gender(self, response):
        return self.gender_lookup(self.product_name(response), greedy=True)

    def product_brand(self, response):
        return "Converse"

    def skus(self, response):
        skus = {}
        colour = clean(response.css('#skuColor ::attr(value)'))[0]
        sizes_sel = response.css('#size-select option')[1:]
        common_sku = {"colour": colour}
        common_sku.update(self.product_pricing_common_new(response))

        for size in sizes_sel:
            sku = common_sku.copy()
            size = clean(size.css('[inventory!="0"] ::text'))

            if size:
                sku["size"] = size[0]
                skus[colour + "/" + sku["size"]] = sku
            else:
                sku["out_of_stock"] = True

        return skus


class ConverseCrawlSpider(BaseCrawlSpider):

    listing_css = [
        '.navigation-expanded a',
        '[title="next"]'
    ]
    product_css = '.p-l-name a'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")
    )


class ConverseParseSpiderCN(MixinCN, ConverseParseSpider):
    name = MixinCN.retailer + "-parse"


class ConverseCrawlSpiderCN(MixinCN, ConverseCrawlSpider):
    name = MixinCN.retailer + "-crawl"
    parse_spider = ConverseParseSpiderCN()
