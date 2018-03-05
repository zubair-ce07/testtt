from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class MixinCN:
    retailer = "converse-cn"
    start_urls = ["http://www.converse.com.cn/"]
    allowed_domain = ["www.converse.com.cn"]
    market = "CN"

    MERCH_INFO = [
        "限量版",
    ]


class ConverseParseSpider(BaseParseSpider):

    brand_map = [
        "CONVERSE X NBA",
        "Converse"
    ]

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
        garment["merch_info"] = self.merch_info(response)

        if not garment["skus"]:
            garment.update(self.product_pricing_common_new(response))
            garment["out_of_stock"] = True

        return garment

    def product_id(self, response):
        return clean(response.css('#skuCode ::attr(value)'))[0]

    def raw_name(self, response):
        raw_name = clean(response.css('.product-name ::text'))
        return ''.join(raw_name)

    def product_name(self, response):
        raw_name = self.raw_name(response)
        name = raw_name.split('】')[1] if "】" in raw_name else raw_name

        return name.replace(self.product_brand(response), '')

    def merch_info(self, response):
        title = clean(response.css('title ::text'))[0]
        return [m for m in self.MERCH_INFO if m in title]

    def image_urls(self, response):
        img_urls = clean(response.css('.product-thumb-list a ::attr(data-img)'))
        return [response.urljoin(img_url.replace('S', "L")) for img_url in img_urls]

    def raw_description(self, response):
        desc_sel = response.css('.product-description')[0]
        raw_desc = clean(desc_sel.css('li ::text, p[style] ::text'))[0]
        return raw_desc.split('. ')

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def product_gender(self, response):
        return self.gender_lookup(self.raw_name(response), greedy=True)

    def product_brand(self, response):
        brand = [brand for brand in self.brand_map if brand in self.raw_name(response)]
        return ''.join(brand) if brand else "converse"

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
                sku["size"] = self.one_size if size[0] == "OS" else size[0]
                skus[colour + "/" + sku["size"]] = sku
            else:
                sku["out_of_stock"] = True

        return skus


class ConverseCrawlSpider(BaseCrawlSpider):

    listing_css = [
        '.navigation-expanded',
        '[title="next"]'
    ]
    product_css = '.p-l-name'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")
    )


class ConverseParseSpiderCN(MixinCN, ConverseParseSpider):
    name = MixinCN.retailer + "-parse"


class ConverseCrawlSpiderCN(MixinCN, ConverseCrawlSpider):
    name = MixinCN.retailer + "-crawl"
    parse_spider = ConverseParseSpiderCN()
