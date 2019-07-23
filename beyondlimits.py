from datetime import datetime

from scrapy import Request, Spider
from scrapy_spider.items import BeyondLimitItem


class CrawlSpider(Spider):
    name = 'beyondlimitspider'
    allowed_domains = ['beyondlimits.com']
    start_urls = [
        'https://www.beyondlimits.com/Sales/Men/#bb_artlist',
        'https://www.beyondlimits.com/Sales/Women/'
    ]
    retailer = 'beyondlimits-gb'
    market = 'UK'
    language = 'English'
    gender = ['Men', 'Women']

    def get_product_sku(self, response):
        skus = {}
        css_size = "option:not(:first-child)::text"
        product_size = response.css(css_size).getall()

        if product_size:
            css_price = ".price span::text"
            css_sku_id = "small.bb_art--artnum span::text"
            css_color = ".bb_boxtxt--content ul > li:first-child::text"
            css_currency = "div.price meta::attr(content)"

            price_color = {
                'price': response.css(css_price).get().split(" ", 1)[0],
                'sku_id': response.css(css_sku_id).get(),
                'color': response.css(css_color).get().split(" ", 1)[1],
                'currency': response.css(css_currency).get(),
                'sku_color': response.css(css_color).get().split(" ", 1)[1].capitalize().replace(' ', '_')
            }

            for sizes in product_size:
                current_sku = {f"{price_color['sku_color']}_{sizes}": {'price': price_color['price'],
                                                                       'currency': price_color['currency'],
                                                                       'size': sizes,
                                                                       'color': price_color['color']}}
                skus.update(current_sku)
        return skus

    def parse(self, response):
        css_single_product = ".bb_product--imgwrap > a::attr(href)"
        links = response.css(css_single_product).getall()
        for link in links:
            yield Request(link, callback=self.parse_of_clothing_item)

        css_pagination = "a.bb_pagination--item::attr(href)"
        next_page = response.css(css_pagination).getall()
        for link in next_page:
            yield Request(link, callback=self.parse)

    def parse_of_clothing_item(self, response):
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
        return next(gender for gender in self.gender if gender in response.url)
