import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from woolsworth.items import Product


class WoolsworthSpider(CrawlSpider):
    name = 'woolsworth'
    allowed_domains = ['www.woolworths.co.za']

    # start_urls = [
    #     'http://www.woolworths.co.za/store/cat/Kids/_/N-1z13s2t']

    # rules = (
    #     Rule(LinkExtractor(
    #         restrict_xpaths='//span[@class="icon icon--right-dark"]/parent::a')),
    #     Rule(LinkExtractor(
    #         restrict_css="a.product-card__details"), callback="parse_product"),)

    def start_requests(self):
        start_urls = [
            'http://www.woolworths.co.za/store/prod/Women/Clothing/New-Arrivals/Metallic-Textured-Slip-Dress/_/A-503949756',
            'http://www.woolworths.co.za/store/prod/Kids/Boys/Underwear-Socks/Batman-Socks-3-Pack/_/A-503555910',
            'http://www.woolworths.co.za/store/prod/Kids/Boys/Tops-Tees/Lightning-Knit/_/A-503777870',
            'http://www.woolworths.co.za/store/prod/Kids/Boys/Bottoms/Adjustable-Bermuda-Shorts/_/A-503771730']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        product = Product()
        self.url(response, product)
        self.product_name(response, product)
        self.brand(response, product)
        self.retailer_id(response, product)
        self.details(response, product)
        yield product

    @staticmethod
    def url(response, product):
        product['url'] = response.url

    @staticmethod
    def product_name(response, product):
        product['name'] = response.css('h1::text').extract_first().strip()

    @staticmethod
    def brand(response, product):
        if response.css('meta[itemprop="brand"]::attr(content)').extract_first():
            product['brand'] = response.css('meta[itemprop="brand"]::attr(content)').extract_first().strip()

    @staticmethod
    def retailer_id(response, product):
        product['retailer_id'] = response.css('meta[itemprop="productId"]::attr(content)').extract_first().strip()

    @staticmethod
    def details(response, product):
        details_div = response.css('h4.accordion__toggle--chrome + div')[0]
        details = []
        if details_div.css('p::text'):
            print(details_div.css('p::text').extract_first().strip())
            details.append(details_div.css('p::text').extract_first().strip())

        if details_div.css('ul:not([class])'):
            print(details_div.css('ul:not([class]) li::text').extract())
            details.append(details_div.css('ul:not([class]) li::text').extract())

        # details_div.css('ul')[0].css('li::text').extract()

        product['details'] = details
