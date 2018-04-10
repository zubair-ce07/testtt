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

    living_category = 'wohnen'
    new_category = 'neu'

    xpath_categories = ("//main[@id='content-wrapper']"
                        "/div[@class='container-fluid page-max-width']"
                        "//a[not(contains(@class,'product-list-tile-holder'))]"
                        "[not(.//p[text()='My Home'])]")
    required_categories = ("main#content-wrapper > div.container-fluid "
                           "a:not(.product-list-tile-holder):not(:contains('My Home')), "
                           "a:not(.product-list-tile-holder):contains('My Home ')")
    required_products = "a.product-list-tile-holder"

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
            deny=(living_category,)),
             callback='parse_additional_products',
             follow=True
            ),
        Rule(LinkExtractor(
            restrict_css=required_products,
             deny=(living_category,)),
             callback='parse_product'
            ),
    )

    def start_requests(self):
        #yield Request('https://www.ernstings-family.de', callback=self.parse)
        #yield Request('https://www.ernstings-family.de//navigation.json?storeId=10151',
        #              callback=self.parse_navigation_links)
        yield Request('https://www.ernstings-family.de/sale-jungen-kleinkinder-98-128/jungen-langarmshirt-mit-applikation-79311.html',
                      callback=self.parse_product)

    def parse_navigation_links(self, response):
        navigations = json.loads(response.text)
        required_headers = []
        link_extractor_re = re.compile("'href': u'(.*?)'")

        for header in navigations['navigation']:
            if header['name'].lower() not in [self.living_category, self.new_category]:
                required_headers.append(str(header))

        for header in required_headers:
            extracted_links = link_extractor_re.findall(header)
            for link in extracted_links:
                if link:
                    yield Request(link, callback=self.parse)

    def parse_additional_products(self, response):
        pagination = response.css(
            "main#content-wrapper > div.container-fluid span#product-list-load-more-products"
        )

        if not pagination:
            return

        store_id = self.get_js_element(response, 'storeId')
        catalog_id = self.get_js_element(response, 'catalogId')
        products_per_page = self.get_js_element(response, 'productListPageSizeOfPage')
        products_list_pages = self.get_js_element(response, 'productListPageReloadBoundary')
        category_id = self.get_js_element(response, 'categoryId')
        search_type = self.get_search_type(response)

        products_list_url = (
            "https://www.ernstings-family.de/wcs/resources/store/{}/productview"
            "/bySearchTermDetails/*?pageNumber={}&pageSize={}&pageSizeReloadBoundary={}"
            "&searchType={}&categoryId={}&profileName=EF_findCatalogEntryByNameAndShort"
            "Description_Details"
        )

        for page_number in range(2, int(products_list_pages) + 1):
            products_list_json = products_list_url.format(
                store_id, page_number, products_per_page,
                products_list_pages, search_type, category_id
            )
            yield Request(products_list_json, callback=self.parse_json_products,
                          meta={'catalog_id': catalog_id, 'store_id': store_id})

    def parse_json_products(self, response):
        catalog_id = response.meta.get('catalog_id')
        store_id = response.meta.get('store_id')
        all_products = json.loads(response.text)
        product_url_template = (
            "https://www.ernstings-family.de/ProductDisplay?urlRequestType=Base"
            "&catalogId={}&productId={}&storeId={}"
        )

        for product in all_products['CatalogEntryView']:
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
        scripts = response.css('script ::text')
        breadcrumbs = json.loads(scripts.re_first('var globalBreadcrumbs = (.+?);'))
        category = []
        for label_key in sorted(breadcrumbs):
            category.append(breadcrumbs[label_key]['label'])
        return category

    def get_gender(self, categories):
        for category in categories:
            for gender_key in self.genders:
                if gender_key in category.lower():
                    return self.genders[gender_key]
        return 'unisex-adults'

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


def get_cents_price(price_with_currency):
    price = re.search(r'(\d+),(\d+)', price_with_currency).group(0)
    return int(float(price.replace(',', '.')) * 100)


def clean(formatted):
    if not formatted:
        return formatted
    if isinstance(formatted, list):
        cleaned = [re.sub(r'\s+', ' ', each).strip() for each in formatted]
        return list(filter(None, cleaned))
    return re.sub(r'\s+', ' ', formatted).strip()
