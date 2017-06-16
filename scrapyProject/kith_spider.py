from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class KithSpider(CrawlSpider):
    name = "kith"
    start_urls = ['https://kith.com/', 'https://kith.com/pages/women/', 'https://kith.com/pages/kids/']
    allowed_domains = ['kith.com']
    DOWNLOAD_DELAY = 0.5
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul/li[@class="main-nav-list-item"]')),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="product-card-info"]'), callback="parse_products", follow=True),
    )

    def parse_products(self, response):
        yield {
            'description': self.get_description(response),
            'image-urls': response.xpath('//div[@class="super-slider-thumbnails-slide-wrapper"]/img/@src').extract(),
            'name': response.xpath('//h1[@class="product-header-title"]/span/text()').extract_first().strip(),
            'retailer_sku': response.xpath(
                '//div[@id="notify-wrapper"]/form/input[@id="product_id"]/@value').extract_first(),
            'skus': self.get_skus(response),
            'gender': self.get_gender(response),
            'url': response.url
        }

    def get_gender(self, response):
        product_name = response.xpath('//h1[@class="product-header-title"]/span/text()').extract_first().strip()
        if "Kidset" in product_name:
            return "kids"
        product_name = response.xpath('//nav[@class="breadcrumb text-center"]/a/@href').extract_first().strip()
        if "women" in product_name:
            return "female"
        else:
            return "male"


    def get_description(self, response):
        description1 = response.xpath('//div[@class="product-single-details-dropdown"]/div/p/text()').extract()
        description2 = response.xpath('//div[@class="product-single-details-dropdown"]/div/ul/li/text()').extract()
        description = description1 + description2
        description = [info.strip().replace('\xa0', '') for info in description if info != '\xa0']
        return description

    def get_skus(self, response):
        skus = {}
        sizes = response.xpath('//div[@class="product-single-form-wrapper"]/form/div/select/option/text()').extract()
        product_ids = response.xpath(
            '//div[@class="product-single-form-wrapper"]/form/div/select/option/@value').extract()
        currency = response.xpath('//div[@class="product-single-header"]/meta/@content').extract_first()
        color = response.xpath('//div[@class="product-single-header"]/div/span/text()').extract_first().strip()
        price = response.xpath('//span[@class="product-header-title -price"]/@content').extract_first()
        for product_id, size in zip(product_ids, sizes):
            skus[product_id] = {}
            skus[product_id]["colour"] = color
            skus[product_id]["currency"] = currency
            skus[product_id]["price"] = price
            skus[product_id]["size"] = size.strip()
        return skus

