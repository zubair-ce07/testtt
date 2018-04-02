"""
Spider to crawl all products in ernstings-family.de website
Example command from terminal: $ scrapy crawl ernstings -o ernstings.json
Pylint score: 10.00
"""

import json
import re
import scrapy                                       # pylint: disable=import-error
from scrapy.spiders import Rule, CrawlSpider        # pylint: disable=import-error
from scrapy.linkextractors import LinkExtractor     # pylint: disable=import-error
from scrapy_task.items import Product, StoreKeepingUnits


class ErnstingsSpider(CrawlSpider):
    """Spider to crawl all products in ernstings-family.de website"""

    name = "ernstings"
    allowed_domains = ['ernstings-family.de']
    ids = []

    rules = (
        Rule(LinkExtractor(
            restrict_css=("main#content-wrapper > div.container-fluid "
                          "a:not([class*='product-list-tile-holder']):not(:contains('My Home')), "
                          "a:not([class*='product-list-tile-holder']):contains('My Home ')"),
            deny=('(.*?)wohnen(.*?)', )),
             callback='more_products',
             follow=True
            ),
        Rule(LinkExtractor(
            restrict_css="div.teaser-highlight-product-wrapper a.link-blank",
            deny=('(.*?)wohnen(.*?)', )),
             callback='parse_product'
            ),
        Rule(LinkExtractor(
            restrict_css="a[class*='product-list-tile-holder']",
            deny=('(.*?)wohnen(.*?)', )),
             callback='parse_product'
            ),
    )

    def start_requests(self):
        """Manually defining it, because the links in hover of navigation bar are
        not available in homepage"""
        yield scrapy.Request('https://www.ernstings-family.de')
        yield scrapy.Request('https://www.ernstings-family.de//navigation.json?storeId=10151',
                             self.parse_json_links)

    @staticmethod
    def parse_json_links(response):
        """Extract links from navigation json page"""
        navbar_dict = json.loads(response.text)
        navbar_texts = []

        for navbar in navbar_dict['navigation']:
            if navbar['name'] != 'Wohnen' and navbar['name'] != 'NEU':
                navbar_texts.append(str(navbar))

        for dict_text in navbar_texts:
            nav_links = re.findall("'href': u'(.+?)'", dict_text)
            for nav_link in nav_links:
                yield scrapy.Request(nav_link)

    def more_products(self, response):
        """Method to get more products from json page, if more products button is there"""
        more = response.css(
            "main#content-wrapper > div.container-fluid span#product-list-load-more-products"
        )

        if more:
            store_id = self.get_js_element(response, 'storeId')
            catalog_id = self.get_js_element(response, 'catalogId')
            products_per_page = self.get_js_element(response, 'productListPageSizeOfPage')
            products_list_pages = self.get_js_element(response, 'productListPageReloadBoundary')
            category_id = self.get_js_element(response, 'categoryId')
            search_type = self.get_search_type(response)

            for num in range(2, int(products_list_pages) + 1):
                load_products_url = (
                    "https://www.ernstings-family.de/wcs/resources/store/{}/productview"
                    "/bySearchTermDetails/*?pageNumber={}&pageSize={}&pageSizeReloadBoundary={}"
                    "&searchType={}&categoryId={}&profileName=EF_findCatalogEntryByNameAndShort"
                    "Description_Details"
                ).format(
                    store_id, num, products_per_page, products_list_pages, search_type, category_id
                )
                yield scrapy.Request(load_products_url, self.parse_json_products,
                                     meta={'catalog_id': catalog_id, 'store_id': store_id})

    def parse_json_products(self, response):
        """Method to make the links for products having data in json file"""
        catalog_id = response.meta.get('catalog_id')
        store_id = response.meta.get('store_id')
        products_dict = json.loads(response.text)

        for product in products_dict['CatalogEntryView']:
            product_id = product['uniqueID']
            product_url = (
                "https://www.ernstings-family.de/ProductDisplay?urlRequestType=Base"
                "&catalogId={}&productId={}&storeId={}"
            ).format(catalog_id, product_id, store_id)

            yield scrapy.Request(product_url, self.parse_product)

    def parse_product(self, response):
        """Method to parse a product and get required details"""

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
            sku['currency'] = self.get_js_element(response, 'commandContextCurrency')
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

    @staticmethod
    def get_search_type(response):
        """Method to get searchtype"""
        javascripts = response.css('script ::text').extract()
        search_type = None
        for each in javascripts:
            text = re.search(r"var searchType = '(\d+)'", each)
            if text:
                search_type = text.group(1)
        return search_type

    @staticmethod
    def get_js_element(response, element):
        """Method to get JavaScript Elements"""
        javascripts = response.css('script ::text').extract()
        value = None
        for each in javascripts:
            text = re.search(r'"{}": "(\w+)"'.format(element), each)
            if text:
                value = text.group(1)
        return value


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
