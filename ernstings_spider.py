"""
Spider to crawl all products in ernstings-family.de website
Example command from terminal: $ scrapy crawl ernstings -o ernstings.json
Pylint score: 10.00
"""

import re
from scrapy.spiders import Rule, CrawlSpider        # pylint: disable=import-error
from scrapy.linkextractors import LinkExtractor     # pylint: disable=import-error
from scrapy_task.items import Product, StoreKeepingUnits


class ErnstingsSpider(CrawlSpider):
    """Spider to crawl all products in ernstings-family.de website"""
    name = "ernstings"
    allowed_domains = ['ernstings-family.de']
    start_urls = ['https://www.ernstings-family.de']
    ids = []

    rules = (
        Rule(LinkExtractor(
            restrict_css="div#main-navigation-wrapper a:not(:contains('Wohnen'))"
            )),
        Rule(LinkExtractor(
            restrict_css=("main#content-wrapper > div.container-fluid "
                          "a:not([class*='product-list-tile-holder']):not(:contains('My Home')), "
                          "a:not([class*='product-list-tile-holder']):contains('My Home ')")
            )),
        Rule(LinkExtractor(
            restrict_css="div.teaser-highlight-product-wrapper a.link-blank"),
             callback='parse_product'
            ),
        Rule(LinkExtractor(
            restrict_css="a[class*='product-list-tile-holder']"),
             callback='parse_product'
            ),
    )

    def parse_product(self, response):
        """Parsing product and getting required details"""

        product_id = self.get_retailer_sku(response)

        if product_id not in self.ids:
            self.ids.append(product_id)

            product = Product()
            product['retailer_sku'] = product_id
            product['category'] = self.get_category(response)
            product['gender'] = self.get_gender(product['category'])
            product['brand'] = self.get_brand(response)
            product['url'] = response.url
            product['name'] = self.get_name(response)
            product['description'] = self.get_description(response)
            product['care'] = self.get_care(response)
            product['image_urls'] = self.get_images(response)
            product['skus'] = self.get_skus(response)

            yield product

    @staticmethod
    def get_retailer_sku(response):
        """Method to get retailer sku"""
        retailer_sku = response.css("meta[name='pageIdentifier']::attr(content)").extract()
        return remove_formatting(retailer_sku)

    @staticmethod
    def get_category(response):
        """Method to get category"""
        javascripts = response.css('script ::text').extract()
        category = []
        for each in javascripts:
            for num in range(6):
                label = re.search('"{}":(.+?)"label":"(.+?)"'.format(num), each)
                if label:
                    category.append(label.group(2))
        return category

    @staticmethod
    def get_gender(category):
        """Method to get gender"""
        gender = None
        for each in category:
            if not gender:
                if re.search('(M|m)\xe4dchen', each):
                    gender = 'girls'
                elif re.search('(J|j)ungen', each):
                    gender = 'boys'
                elif re.search('(D|d)amen', each):
                    gender = 'women'
                elif re.search('(H|h)erren', each):
                    gender = 'men'
                elif re.search('((N|n)ewborn)|((B|b)aby)', each):
                    gender = 'unisex-kids'
        if not gender:
            gender = 'unisex-adults'
        return gender

    @staticmethod
    def get_brand(response):
        """Method ot get brand"""
        brand = response.css('img.brand-logo::attr(alt)').extract()
        return remove_formatting(brand)

    @staticmethod
    def get_name(response):
        """Method to get name"""
        name = response.css('h1.product-detail-product-name::text').extract()
        return remove_formatting(name)

    @staticmethod
    def get_images(response):
        """Method to get images urls"""
        images = response.css('img.product-view-slide-image::attr(src)').extract()
        return ['https:{}'.format(image) for image in images]

    @staticmethod
    def get_description(response):
        """Method to get description"""
        desc = response.css('div.product-detail-information-contents p::text, li::text').extract()
        return remove_formatting(desc)

    @staticmethod
    def get_care(response):
        """Method to get care instructions"""
        care = response.css('div.care-icon-text-wrapper div.text-holder::text').extract()
        return remove_formatting(care)

    @staticmethod
    def get_prices(response):
        """Method to get prices"""
        prices = response.css('span.product-price::text').extract()
        price = None
        previous = []
        if len(prices) < 2:
            price = get_float_price(remove_formatting(prices))
        else:
            prices = remove_formatting(prices)
            previous.append(get_float_price(prices[0]))
            price = get_float_price(prices[1])
        return price, previous

    @staticmethod
    def get_currency(response):
        """Method to get currency"""
        javascripts = response.css('script ::text').extract()
        currency = None
        for each in javascripts:
            text = re.search(r'"commandContextCurrency": "(\w+)"', each)
            if text:
                currency = text.group(1)
        return currency

    @staticmethod
    def get_colour(response):
        """Method to get color"""
        colour = response.css('p.product-detail-product-color::text').extract()
        return remove_formatting(colour)

    def get_skus(self, response):
        """Method to get SKUs"""
        options = response.css('select#select-size-product-detail option')
        skus = []
        for option in options:
            sku = StoreKeepingUnits()
            sku['price'], sku['previous_prices'] = self.get_prices(response)
            sku['currency'] = self.get_currency(response)
            sku['colour'] = self.get_colour(response)
            size = option.css('option::text').extract_first()
            sku['size'] = None
            if size != '-':
                sku['size'] = size
            if option.css('option[disabled]'):
                sku['out_of_stock'] = True
            sku['sku_id'] = option.css('option::attr(data-catentry-id)').extract_first()
            skus.append(sku)
        return skus


def get_float_price(price):
    """Function to extract price in float format from string"""
    tens, decimals = re.search(r'(\d+),(\d+)', price).group(1, 2)
    return float('{}.{}'.format(tens, decimals))


def remove_formatting(texts):
    """Function to remove \n \t and trailing spaces etc and return pure text (if any)"""
    pure_text = []
    for each in texts:
        text = re.sub(r'\s+', ' ', each).strip()
        if text:
            pure_text.append(text)
    if not pure_text:
        pure_text = None
    elif len(pure_text) == 1:
        pure_text = pure_text[0]
    return pure_text
