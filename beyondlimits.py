from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy import Request
from scrapy_spider.items import BeyondLimitItem


class BeyondLimitsSpider(CrawlSpider):
    name = 'beyondlimitspider'
    allowed_domains = ['beyondlimits.com']
    start_urls = [
        'https://www.beyondlimits.com/Men/',
        'https://www.beyondlimits.com/Women/'
    ]
    retailer = 'beyondlimits-uk'
    market = 'UK'
    language = 'en'
    gender = ['Men', 'Women', 'Unisex-adults']
    default_gender = 'Unisex-adults'

    def get_product_sku(self, response):
        skus = {}
        color_css = ".bb_boxtxt--content ul > li:first-child::text"
        size_css = "option:not(:first-child)::text"

        price = self.get_product_price(response)
        common_sku = {
            'color': response.css(color_css).get().split(" ", 1)[1],
        }
        common_sku.update(price)
        color = common_sku['color'].capitalize().replace(' ', '_')
        product_sizes = response.css(size_css).getall()

        for size in product_sizes:
            sku = common_sku.copy()
            sku['size'] = size
            current_sku = {f"{color}_{size}": sku}
            skus.update(current_sku)

        return skus

    def parse(self, response):
        product_css = ".bb_product a::attr(href)"
        product_url = response.css(product_css).getall()
        for link in product_url:
            yield Request(link, callback=self.parse_item)

        pagination_css = "a.bb_pagination--item::attr(href)"
        next_page = response.css(pagination_css).getall()
        if next_page:
            yield Request(next_page[0], callback=self.parse)

    def parse_item(self, response):
        garment = BeyondLimitItem()
        garment["name"] = self.get_product_name(response)
        garment["skus"] = self.get_product_sku(response)
        garment["gender"] = self.get_gender(response)
        garment["description"] = self.get_product_description(response)
        garment["retailer_sku"] = self.get_retailer_sku(response)
        garment["image_urls"] = self.get_image_urls(response)
        garment["care"] = self.get_product_care(response)
        garment["lang"] = self.language
        garment["brand"] = self.get_product_brand(response)
        garment["category"] = self.get_product_category(response)
        garment["url"] = response.url
        garment["crawl_start_time"] = datetime.now().isoformat()
        garment["date"] = int(datetime.timestamp(datetime.now()))
        garment["crawl_id"] = self.get_crawl_id()
        garment["market"] = self.market
        garment["retailer"] = self.retailer

        yield garment

    def get_product_name(self, response):
        css = ".bb_art--header h1::text"
        return response.css(css).get()

    def get_product_description(self, response):
        css = "header.bb_art--header p::text"
        return response.css(css).get()

    def get_retailer_sku(self, response):
        css = "small.bb_art--artnum span::text"
        return response.css(css).get()

    def get_image_urls(self, response):
        css = "a.bb_pic--navlink::attr(href)"
        return response.css(css).getall()

    def get_product_care(self, response):
        css = ".bb_boxtxt--content ul > li:not(:first-child)::text"
        return ' '.join(response.css(css).getall())

    def get_product_category(self, response):
        css = "span.bb_breadcrumb--item.is-last strong::text"
        return response.css(css).get()

    def get_crawl_id(self):
        return f"{self.retailer}-{datetime.now().strftime('%Y%m%d-%H%M%s')}-medp"

    def get_product_brand(self, response):
        css = ".ft_logo--inner img::attr(title)"
        return response.css(css).get()

    def get_gender(self, response):
        return next(gender for gender in self.gender if gender in response.url) or self.default_gender

    def get_product_price(self, response):
        price_css = ".price span::text"
        currency_css = "div.price meta::attr(content)"
        old_price_css = '.bb_art--pricecontent  del::text'
        return {'price': response.css(price_css).get().split(" ", 1)[0],
                'currency': response.css(currency_css).get(),
                **({'old price': response.css(old_price_css).get().split(" ", 1)[0]}
                   if response.css(old_price_css).get() else {})
                }
