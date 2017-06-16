import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class HypeDC(scrapy.Spider):
    name = "hypedc"
    start_urls = [
        'https://www.hypedc.com/',
    ]
    products_name_repository = []

    def parse(self, response):
        extractor = LinkExtractor(allow=(), allow_domains='hypedc.com')
        links = extractor.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_item)

    def parse_item(self, response):
        for product_url in response.css('div.item > a::attr(href)').extract():
            yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        identifier = self.get_identifier(response)
        if identifier not in self.products_name_repository:
            self.products_name_repository.append(identifier)
            yield {
                'Brand': self.get_brand(response),
                'Name': self.get_name(response),
                'Gender': self.get_gender(response),
                'Description': self.get_description(response),
                'Other Colors': self.get_other_colors(response),
                'Breadcrumb': self.get_breadcrumb(response),
                'Img-Src': self.get_img_src(response),
                'URL': self.get_url(response),
                'Skus': self.get_skus(response),
            }
        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse_product)

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

    def get_img_src(self, response):
        return response.css('div.slider-inner div.unveil-container noscript img::attr(src)').extract()

    def get_url(self, response):
        return response.url

    def get_gender(self, response):
        return response.css('ul.breadcrumb li a span::text').extract()[1]

    def get_skus(self, response):
        skus = {}
        currency = response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()
        price = response.css('div.price-div meta::attr(content)').extract_first()
        color = (response.css('h3.product-colour::text').extract_first()).strip()
        size_groups = response.css('div#product-options-wrapper > ul#size-selector-desktop-tabs li a::text').extract()
        size_selectors = response.css('div.tab-content div.tab-pane::attr(id)').extract()
        sizes = []
        for s in size_selectors:
            sizes.append(response.css('div.tab-content div#' + s + ' ul li[data-stock="in"] a::text').extract())
        for g in size_groups:
            for size in sizes:
                for s in size:
                    skus[color + g + s] = {}
                    skus[color + g + s]["colour"] = color
                    skus[color + g + s]["currency"] = currency
                    skus[color + g + s]["price"] = price
                    skus[color + g + s]["size"] = s
        return skus
