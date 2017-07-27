import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from hypedc.items import HypedcItem
from itertools import product


class HypeDCSpider(CrawlSpider):
    name = "hypedc"
    start_urls = [
        'https://www.hypedc.com/',
    ]
    products_name_repository = []
    extractor = LinkExtractor(restrict_css='ul.nav-primary > li[id] a', allow_domains='hypedc.com')
    rules = (Rule(extractor), Rule(LinkExtractor(restrict_css='div.item'), callback="parse_product"))

    def parse_product(self, response):
        identifier = self.get_identifier(response)
        if identifier not in self.products_name_repository:
            self.products_name_repository.append(identifier)
            product = HypedcItem()
            product['brand'] = self.get_brand(response)
            product['name'] = self.get_name(response)
            product['category'] = self.get_gender(response)
            product['other_colors'] = self.get_other_colors(response)
            product['breadcrumb'] = self.get_breadcrumb(response)
            product['images'] = self.get_images(response)
            product['url'] = response.url
            product['skus'] = self.get_skus(response)
            yield product

    def get_identifier(self, response):
        name = response.css('h1.product-name::text').extract_first()
        identifier = self.start_urls[0] + name
        return identifier

    def get_brand(self, response):
        return response.css('h2.product-manufacturer::text').extract_first()

    def get_name(self, response):
        return response.css('h1.product-name::text').extract_first()

    def get_other_colors(self, response):
        return response.css('div.container div#carousel-colours div.row div.col-sm-24 div.carousel-inner '
                            'div:first-child div.category-products div.item a div.product-info div h5::text').extract()

    def get_description(self, response):
        return response.css('div.product-description::text').extract_first().strip()

    def get_breadcrumb(self, response):
        return response.css('ul.breadcrumb li a span::text').extract()

    def get_images(self, response):
        return response.css('div.slider-inner div.unveil-container noscript img::attr(src)').extract()

    def get_gender(self, response):
        return response.css('ul.breadcrumb li a span::text').extract()[1]

    def get_skus(self, response):
        skus = {}
        currency = response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()
        price = response.css('div.price-div meta::attr(content)').extract_first()
        color = response.css('h3.product-colour::text').extract_first().strip()
        size_groups = response.css('div#product-options-wrapper > ul#size-selector-desktop-tabs li a::text').extract()
        size_selectors = response.css('div.tab-content div.tab-pane::attr(id)').extract()
        size_css_selector = 'div.tab-content div#{} ul li[data-stock="in"] a::text'
        sizes = list(map(lambda selector: response.css(size_css_selector.format(selector)).extract(), size_selectors))
        for group, size in product(size_groups, sizes):
            for size_individual in size:
                skus[color + group + size_individual] = {"colour": color, "currency": currency,
                                                         "price": price, "size": size_individual}
        return skus

