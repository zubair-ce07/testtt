from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import BognerItem


class BognerSpider(CrawlSpider):
    name = "bogner"

    allowed_domains = ['bogner.com']
    start_urls = [
        'https://www.bogner.com/en-gb/women.html'
    ]

    pagination_xpath = '//div[@class="toolbar-bottom"]//a[@class="next i-next"]'
    navbar_xpath = '//nav[@id="nav"]//li[@class="level2   "]//a'
    product_xpath = '//a[@class="product-image is-visible-default"]'
    rules = (
        Rule(LinkExtractor(allow=("/women", "/men",), restrict_xpaths=[navbar_xpath, pagination_xpath])),
        Rule(LinkExtractor(restrict_xpaths=product_xpath), callback='parse_item'),
    )

    gender_list = ['Men', 'Women', 'Kids', 'Unisex']

    retailer_skus_all = set()

    def parse_item(self, response):
        retailer_sku = self.extract_retailer_sku(response)
        if not self.check_if_parsed(retailer_sku):
            yield self.make_new_item(response, retailer_sku)

    def check_if_parsed(self, retailer_sku):
        if retailer_sku in self.retailer_skus_all:
            return True
        self.retailer_skus_all.add(retailer_sku)
        return False

    def make_new_item(self, response, retailer_sku):
        items = BognerItem()
        items['url'] = response.url
        items['retailer_sku'] = retailer_sku
        items['category'] = self.extract_category(response)
        items['gender'] = self.extract_gender(items['category'])
        items['brand'] = self.extract_brand(response)
        items['name'] = self.extract_name(response)
        items['description'] = self.extract_description(response)
        items['care'] = self.extract_care(response)
        items['image_urls'] = self.extract_image_urls(response)
        items['price'] = self.extract_price(response)
        items['currency'] = "GBP"
        items['retailer'] = self.extract_retailer(response)
        items['market'] = items['retailer'].split(' ')[-1]
        items['skus'] = self.extract_skus(response, items['price'])
        return items

    def extract_retailer_sku(self, response):
        return response.xpath('//p[@class="sku"]/text()').re_first('\d+')

    def extract_category(self, response):
        return response.xpath('//div[@class="breadcrumbs"]/ul/li/a/span/text()')[1:].getall()

    def extract_brand(self, response):
        return response.xpath('//h2[@class="collection-name"]/text()').get()

    def extract_name(self, response):
        return response.xpath('//h1[@class="product-name-text"]/text()').get().strip()

    def extract_gender(self, category):
        if category:
            if category[0] in self.gender_list:
                return category[0]
        return 'Unisex'

    def extract_retailer(self, response):
        return response.xpath('//title/text()').re_first('\|.*').split('|')[-1].strip()

    def extract_description(self, response):
        note = response.css('.std p::text').get()
        details = response.xpath('//div[@class="accordion-content-container"]/'
                               'div[@class="product-features"]/ul/li/text()').getall()
        description = [d for d in note.split('.') if d.strip()] + details
        return description

    def extract_care(self, response):
        care_xpath = response.xpath('//div[@class="accordion-content-container"]/div[@class="material-care-container"]')
        return care_xpath.xpath('./div[@class="material-composition-container"]/p/text() | '
                                './div[@class="material-care-tip"]/ul/li/p/text()').getall()

    def extract_image_urls(self, response):
        return response.xpath('//div[@class="view-gallery-slider is-unified-slider"]/div/div/img/@data-src').getall()

    def extract_price(self, response):
        price_xpath = response.xpath('//div[@class="price-container"]')[1]
        price = price_xpath.xpath('./div[@class="price-box"]//span[@class="price"]/text()').re_first('\d+\.?\d*')
        return float(price) * 100

    def extract_skus(self, response, price):
        colours_xpath = response.xpath('//ul[@id="colorswatch-select"]')[1]
        colours = colours_xpath.xpath('.//span/text()').getall()

        sizes_xpath = response.xpath('//div[@id="product-options-wrapper"]//ul[@class="product-sizes"]')
        sizes = []
        availability = []
        if sizes_xpath:
            sizes_xpath = sizes_xpath[1]
            sizes = sizes_xpath.xpath('.//li/@data-size-label').getall()
            availability = sizes_xpath.xpath('.//li/@data-size-availability').getall()
        else:
            sizes.append('ONE-SIZE')
            availability.append('in-stock')

        skus = []
        for colour in colours:
            for size, stock in zip(sizes, availability):
                sku = {
                    'sku_id': f'{colour}_{size}',
                    'price': price,
                    'currency': 'GBP',
                    'size': size,
                    'colour': colour
                }
                if stock == 'sold out':
                    sku['out-of-stock'] = True
                skus.append(sku)
        return skus
