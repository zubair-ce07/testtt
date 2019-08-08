from ..items import Product
from scrapy.spiders import CrawlSpider


class EccoSpiderSpider(CrawlSpider):
    name = 'ecco_spider'
    allowed_domain = 'https://us.ecco.com/'
    start_urls = ['https://us.ecco.com/men/',
                  'https://us.ecco.com/women/']
    lang = 'en'
    market = 'US'
    brand = 'ECCO'
    retailer = 'ecco-usa'
    gender_terms = [
        'Men',
        'Women',
    ]

    def parse(self, response):
        product_css = 'div.product-detail a.product-name'
        product_url = response.css(product_css).getall()
        for url in product_url:
            yield response.follow(url, callback=self.parse_items)

        pagination_css = "div > a.page-next::attr(href)"
        next_page = response.css(pagination_css).getall()
        if next_page:
            yield response.follow(next_page[0], callback=self.parse)

    def parse_items(self, response):

        product = Product()
        product['retailer_sku'] = self.extract_retailer_sku(response)
        product['name'] = self.extract_name(response)
        product['lang'] = self.lang
        product['brand'] = self.brand
        product['gender'] = self.extract_gender(response)
        product['category'] = self.extract_category(response)
        product['retailer'] = self.retailer
        product['url'] = response.url
        product['market'] = self.market
        product['image_urls'] = self.extract_image_urls(response)
        product['description'] = self.extract_description(response)
        product['property'] = self.extract_property(response)
        product['skus'] = self.extract_skus(response)
        yield product

    def extract_shoe_size(self, response):
        css = 'ul#size-wrapper a::text'
        return list(dict.fromkeys(self.clean(response.css(css).getall())))

    def extract_size(self, response):
        css = 'div.size-selector  button::text'
        return list(dict.fromkeys(self.clean(response.css(css).getall())))

    def extract_gender(self, response):
        css = 'a.breadcrumb-element::text'
        gender_clean = self.clean(response.css(css).getall())
        return [gender.lower() for gender in gender_clean if gender in self.gender_terms]

    def extract_skus(self, response):
        skus = []
        colour = self.extract_colour(response)
        common_sku = {
            "price": self.extract_price(response),
            "currency": self.extract_currency(response),
            'colour': colour
        }
        for size in self.extract_size(response):
            for shoe_size in self.extract_shoe_size(response):
                sku = common_sku.copy()
                sku['sku_id'] = f"{size}_{shoe_size}"
                skus.append(sku)

        return skus

    @staticmethod
    def extract_property(response):
        css = 'div.description-list-col ul.bulleted-list li::text'
        return response.css(css).getall()

    @staticmethod
    def extract_description(response):
        css = 'div.description-title > h2::text'
        return response.css(css).get()

    @staticmethod
    def extract_price(response):
        css = 'meta[property="product:price:amount"]::attr(content)'
        return response.css(css).get()

    @staticmethod
    def extract_colour(response):
        css = 'ul#color-wrapper img::attr(alt)'
        return list(dict.fromkeys(response.css(css).extract()))

    @staticmethod
    def extract_currency(response):
        css = 'meta[property="product:price:currency"]::attr(content)'
        return response.css(css).get()

    @staticmethod
    def extract_retailer_sku(response):
        css = 'meta[property="product:retailer_item_id"]::attr(content)'
        return response.css(css).get()

    @staticmethod
    def extract_name(response):
        css = 'div#product-top-info::attr(data-name)'
        return response.css(css).get()

    @staticmethod
    def extract_image_urls(response):
        return response.css('.swiper-slide::attr(style)').re('(?<=url)(.*)(?=)')

    @staticmethod
    def extract_category(response):
        css = 'div#product-top-info::attr(data-categories)'
        return response.css(css).get()

    @staticmethod
    def clean(uncleaned_data):
        return [item.strip() for item in uncleaned_data if item.strip()]
