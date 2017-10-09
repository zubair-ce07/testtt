import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import HunkemollerItem


class HunkemollerProductSpider(CrawlSpider):
    name = 'hunkemollerSpider'
    start_urls = ['https://www.hunkemoller.de/de_de/']

    BRAND = 'Hunkemoller'
    GENDER = 'women'
    LANG = 'de'
    MARKET = 'DE'

    visited_items = set()

    rules = [Rule(LinkExtractor(restrict_css='.nav-container'),
                  callback='parse', follow=True),
             Rule(LinkExtractor(
                 restrict_css='.category-products'),
                 callback='parse_item'),
             ]

    def parse(self, response):
        yield from super(HunkemollerProductSpider, self).parse(response)
        next_url_css = ".pages .next::attr(href)"
        next_url = response.css(next_url_css).extract_first()
        if next_url:
            yield response.follow(
                next_url,
                callback=self.parse
            )

    def parse_item(self, response):
        retailer_sku = self.item_retailer_sku(response)
        if self.is_visited(retailer_sku):
            return
        item = HunkemollerItem()
        item['brand'] = self.BRAND
        item['care'] = self.item_care(response)
        item['category'] = self.item_category(response)
        item['description'] = self.item_description(response)
        item['gender'] = self.GENDER
        item['image_urls'] = self.item_image_urls(response)
        item['name'] = self.item_product_name(response)
        item['retailer_sku'] = retailer_sku
        item['lang'] = self.LANG
        item['market'] = self.MARKET
        item['url'] = response.url
        item['skus'] = self.item_skus(response)
        return item

    def is_visited(self, retailer_sku):
        if retailer_sku in self.visited_items:
            return True
        self.visited_items.add(retailer_sku)
        return False

    def item_care(self, response):
        return response.css(".washing-tips li::text").extract()

    def item_category(self, response):
        category_css = ".breadcrumbs span:first-child::text"
        return response.css(category_css).extract()[1:-1]

    def item_description(self, response):
        description = response.css(".description p::text").extract()
        return [d for d in description if d.strip()]

    def item_image_urls(self, response):
        image_urls = response.css(".scroller a::attr(rel)").extract()
        return list(map(lambda url: eval(url).get("largeimage"), image_urls))

    def item_retailer_sku(self, response):
        retailer_sku_css = ".article-number ::text"
        return response.css(retailer_sku_css).extract_first().split()[1]

    def item_product_name(self, response):
        return response.css(".product-name h1::text").extract_first()

    def item_active_color(self, response):
        color_css = ".pdp-colors .active ::attr(title)"
        return response.css(color_css).extract_first()

    def item_price(self, response):
        price_css = ".price-box span[itemprop]::text"
        price = response.css(price_css).extract_first()
        return int(float(price.strip()) * 100)

    def item_sizes(self, response):
        sizes_dict = {}
        size_selector = response.css(".product-options option[data-products]")
        for selector in size_selector:
            size = selector.css('::text').extract_first().strip()
            c_id = selector.css('::attr(data-products)').extract_first()[2:-2]
            sizes_dict[c_id] = size
        return sizes_dict

    def item_skus(self, response):
        skus = {}
        colour = self.item_active_color(response)
        for s_id, size in self.item_sizes(response).items():
            temp_skus = {}
            temp_skus['colour'] = colour
            temp_skus['currency'] = 'EUR'
            temp_skus['price'] = self.item_price(response)
            temp_skus['size'] = size
            skus[s_id] = temp_skus
        return skus
