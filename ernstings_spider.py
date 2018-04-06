
import json
import re
from collections import OrderedDict
from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy_task.items import Product


class ErnstingsSpider(CrawlSpider):

    name = "ernstings"
    allowed_domains = ['ernstings-family.de']

    living_items_category = 'wohnen'
    new_items_category = 'neu'

    xpath_categories = ("//main[@id='content-wrapper']"
                        "/div[@class='container-fluid page-max-width']"
                        "//a[not(contains(@class,'product-list-tile-holder'))]"
                        "[not(.//p[text()='My Home'])]")
    required_categories = ("main#content-wrapper > div.container-fluid "
                           "a:not([class*='product-list-tile-holder']):not(:contains('My Home')), "
                           "a:not([class*='product-list-tile-holder']):contains('My Home ')")
    required_products = ("a[class*='product-list-tile-holder'], "
                         "div.teaser-highlight-product-wrapper a.link-blank")

    genders = OrderedDict([
        (u'm\xe4dchen', 'girls'),
        (u'jungen', 'boys'),
        (u'damen', 'women'),
        (u'herren', 'men'),
        (u'newborn', 'unisex-kids'),
        (u'baby', 'unisex-kids')
    ])

    rules = (
        Rule(LinkExtractor(
            restrict_css=required_categories,
            # restrict_xpaths=xpath_categories,
            deny=(living_items_category,)),
             callback='has_load_more_products',
             follow=True
            ),
        Rule(LinkExtractor(
            restrict_css=required_products,
             deny=(living_items_category,)),
             callback='parse_product'
            ),
    )

    def start_requests(self):
        yield Request('https://www.ernstings-family.de', callback=self.parse)
        yield Request('https://www.ernstings-family.de//navigation.json?storeId=10151',
                      callback=self.parse_json_links)

    def parse_json_links(self, response):
        whole_json_data = json.loads(response.text)
        filtered_data = []
        link_extractor = "'href': u'(.*?)'"

        for each_data in whole_json_data['navigation']:
            if (each_data['name'].lower() != self.living_items_category and
                    each_data['name'].lower() != self.new_items_category):
                filtered_data.append(str(each_data))

        for each_filtered_data in filtered_data:
            extracted_links = re.findall(link_extractor, each_filtered_data)
            for each_extracted_link in extracted_links:
                if each_extracted_link:
                    yield Request(each_extracted_link, callback=self.parse)

    def has_load_more_products(self, response):
        load_more_products = response.css(
            "main#content-wrapper > div.container-fluid span#product-list-load-more-products"
        )

        if load_more_products:
            store_id = self.get_js_element(response, 'storeId')
            catalog_id = self.get_js_element(response, 'catalogId')
            products_per_page = self.get_js_element(response, 'productListPageSizeOfPage')
            products_list_pages = self.get_js_element(response, 'productListPageReloadBoundary')
            category_id = self.get_js_element(response, 'categoryId')
            search_type = self.get_search_type(response)

            data_url_template = (
                "https://www.ernstings-family.de/wcs/resources/store/{}/productview"
                "/bySearchTermDetails/*?pageNumber={}&pageSize={}&pageSizeReloadBoundary={}"
                "&searchType={}&categoryId={}&profileName=EF_findCatalogEntryByNameAndShort"
                "Description_Details"
            )

            for page_number in range(2, int(products_list_pages) + 1):
                products_data_json_page = data_url_template.format(
                    store_id, page_number, products_per_page,
                    products_list_pages, search_type, category_id
                )
                yield Request(products_data_json_page, callback=self.parse_json_products,
                              meta={'catalog_id': catalog_id, 'store_id': store_id})

    def parse_json_products(self, response):
        catalog_id = response.meta.get('catalog_id')
        store_id = response.meta.get('store_id')
        products_data = json.loads(response.text)
        product_url_template = (
            "https://www.ernstings-family.de/ProductDisplay?urlRequestType=Base"
            "&catalogId={}&productId={}&storeId={}"
        )

        for product in products_data['CatalogEntryView']:
            product_id = product['uniqueID']
            product_url = product_url_template.format(catalog_id, product_id, store_id)

            yield Request(product_url, callback=self.parse_product)

    def parse_product(self, response):

        product = Product()
        product['retailer_sku'] = self.get_retailer_sku(response)
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
        retailer_sku = response.css("meta[name='pageIdentifier']::attr(content)").extract_first()
        return clean(retailer_sku)

    @staticmethod
    def get_category(response):
        javascripts = response.css('script ::text')
        category = []
        for num in range(6):
            label = javascripts.re('"{}":(.+?)"label":"(.+?)"'.format(num))
            if label:
                category.append(label[1])
        return category

    def get_gender(self, categories):
        gender = None
        for category in categories:
            for gender_key in self.genders.keys():
                if not gender and gender_key in category.lower():
                    gender = self.genders[gender_key]
        if not gender:
            gender = 'unisex-adults'
        return gender

    @staticmethod
    def get_brand(response):
        brand = response.css('img.img-fluid.brand-logo::attr(alt)').extract_first()
        return clean(brand)

    @staticmethod
    def get_name(response):
        name = response.css('h1.product-detail-product-name::text').extract_first()
        return clean(name)

    @staticmethod
    def get_images(response):
        images = response.css('img.product-view-slide-image::attr(src)').extract()
        return [response.urljoin(image) for image in images]

    @staticmethod
    def get_description(response):
        desc = response.css('div.product-detail-information-contents '
                            'p::text, li::text').extract()
        return clean(desc)

    @staticmethod
    def get_care(response):
        care = response.css('div.care-icon-text-wrapper div.text-holder::text').extract()
        return clean(care)

    @staticmethod
    def get_prices(response):
        prices = response.css('div.product-detail-price-wrapper '
                              'span.product-price::text').extract()
        prices = clean(prices)
        price = None
        previous = []
        if len(prices) == 1:
            price = get_cents_price(prices[0])
        else:
            previous.append(get_cents_price(prices[0]))
            price = get_cents_price(prices[1])
        return price, previous

    @staticmethod
    def get_colour(response):
        colour = response.css('p.product-detail-product-color::text').extract_first()
        return clean(colour)

    def get_skus(self, response):
        options = response.css('select#select-size-product-detail option')
        skus = []
        for option in options:
            sku = {}
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
        return response.css('script ::text').re_first(r"var searchType = '(\d+)'")

    @staticmethod
    def get_js_element(response, element):
        return response.css('script ::text').re_first(r'"{}": "(\w+)"'.format(element))


def get_float_price(price):
    tens, decimals = re.search(r'(\d+),(\d+)', price).group(1, 2)
    return float('{}.{}'.format(tens, decimals))


def remove_formatting(texts):
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


def get_cents_price(price_with_currency):
    price = re.search(r'(\d+),(\d+)', price_with_currency).group(0)
    return int(float(price.replace(',', '.')) * 100)


def clean(formatted):
    cleaned = None
    if type(formatted) is list:
        cleaned = [re.sub(r'\s+', ' ', each).strip() for each in formatted]
        cleaned = list(filter(None, cleaned))
    else:
        if formatted:
            cleaned = re.sub(r'\s+', ' ', formatted).strip()
    return cleaned
