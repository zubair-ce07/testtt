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

    visited_urls = set()

    rules = [Rule(LinkExtractor(restrict_css='.nav-container'),
                  callback='parse_pagination', follow=True),
             Rule(LinkExtractor(
                 restrict_css='.category-products'),
                 callback='parse_item')
             ]

    def parse_pagination(self, response):
        next_url_css = ".pages .next::attr(href)"
        next_url = response.css(next_url_css).extract_first()
        if next_url:
            yield response.follow(
                next_url,
                callback=self.parse_pagination
            )

    def parse_item(self, response):
        if self.is_visited(response.url):
            return
        item = HunkemollerItem()
        item['brand'] = self.BRAND
        item['care'] = self.item_care(response)
        item['category'] = self.item_category(response)
        item['description'] = self.item_description(response)
        item['gender'] = self.GENDER
        item['image_urls'] = self.item_image_urls(response)
        item['name'] = self.item_product_name(response)
        item['retailer_sku'] = self.item_retailer_sku(response)
        item['lang'] = self.LANG
        item['market'] = self.MARKET
        item['url'] = response.url
        item['skus'] = self.item_skus(response)
        return item

    def is_visited(self, url):
        if url in self.visited_urls:
            return True
        self.visited_urls.add(url)
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
        size_css = ".product-options option[data-products]::text"
        sizes = response.css(size_css).extract()[1:]
        sizes = [size.strip() for size in sizes if size.strip()]

        c_id_css = ".product-options option[data-products]::attr(data-products)"
        c_ids = response.css(c_id_css).extract()
        c_ids = [i[2:-2] for i in c_ids]
        return dict(zip(c_ids, sizes))

    def item_skus(self, response):
        skus = {}
        colour = self.item_active_color(response)
        for color_id, size in self.item_sizes(response).items():
            temp_skus = {}
            temp_skus['colour'] = colour
            temp_skus['currency'] = 'EUR'
            temp_skus['price'] = self.item_price(response)
            temp_skus['size'] = size
            skus[color_id] = temp_skus
        return skus
