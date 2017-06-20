import scrapy
from scrapy.loader import ItemLoader
from product_scrapper.items import ProductScrapperItem
from urllib.parse import urljoin


class ProductSpider(scrapy.Spider):
    name = "products"
    no_of_products = 1

    def start_requests(self):
        base_url = "http://www.boohoo.com"

        yield scrapy.Request(url=base_url, callback=self.parse)

    def parse(self, response):

        product_by_category = "//div[@class='nav-wrapper']/" \
                            "ul[@class='menu-vertical']/li/a/@href"

        categorized_product_links = response.xpath(product_by_category)

        categorized_product_links = categorized_product_links.extract()

        for link in categorized_product_links:
            yield scrapy.Request(url=link, meta={'products_to_retrieve': 0},
                                 callback=self.get_products)

    def get_products(self, response):
        products_to_retrieve = response.meta['products_to_retrieve']
        product = "//div['search-result-content']/ul/li/div/div[1]/a/@href"
        product_links = response.xpath(product).extract()
        for link in product_links:
            complete_link = urljoin(response.url, link)
            yield scrapy.Request(url=complete_link,
                                 callback=self.retrieve_product_info)

            products_to_retrieve += 1
            if products_to_retrieve >= self.no_of_products:
                return

        # moving onto the next page
        next_page = "//li[@class='pagination-" \
                    "item pagination-item-next']/a/@href"
        next_products_page_link = response.xpath(next_page).extract_first()
        if next_products_page_link:
            yield scrapy.Request(url=next_products_page_link,
                                 meta={'products_to_retrieve':
                                       products_to_retrieve},
                                 callback=self.get_products)

    def retrieve_product_info(self, response):
        name = self.get_name(response)
        product_id = self.get_product_id(response)
        product_desc = self.get_product_desc(response)
        product_care = self.get_product_care(response)
        colors = self.get_colors(response)
        # product_price = self.get_product_price(response)
        url = response.url
        alternate_links = self.get_alternate_links(response)

        products = ItemLoader(item=ProductScrapperItem(), response=response)

        products.add_value('name', name)
        products.add_value('product_desc', product_desc)
        # products.add_value('product_price', product_price)
        products.add_value('url', url)
        products.add_value('product_id', product_id)
        products.add_value('product_care', product_care)

        self.add_image_links(products, colors, product_id)

        language_id = 0
        for link in alternate_links:
            language = self.get_alternate_languages(response)
            yield scrapy.Request(url=link,
                                 meta={
                                       'products': products,
                                       'language': language[language_id],
                                       'colors': colors
                                       },
                                 callback=self.generate_skus)
            language_id += 1

    def generate_skus(self, response):
        product_price = self.get_product_price(response)
        colors = self.get_colors(response)

        products = response.meta['products']
        language = response.meta['language']
        colors = response.meta['colors']

        skus = {}
        skus[language] = {}
        skus[language]['price'] = product_price
        skus[language]['colors'] = []
        for color in colors:
            skus[language]['colors'].append(color.split(':')[1].strip(' '))

        products.add_value('skus', skus)
        return products.load_item()

    def add_image_links(self, products, colors, product_id):
        for color in colors:
            color = color.split(':')[1].strip(' ')

            products.add_value('image_urls', "http://i1.adis.ws/i/"
                               "boohooamplience/" +
                               product_id.lower() + "_" + color.lower() +
                               "_xl?$product_image_main_thumbnail")

            products.add_value('image_urls', "http://i1.adis.ws/i/"
                               "boohooamplience/" +
                               product_id.lower() + "_" + color.lower() +
                               "_xl?$product_image_main")

            for i in range(1, 4):
                products.add_value('image_urls', "http://i1.adis.ws/i/"
                                   "boohooamplience/" +
                                   product_id.lower() +
                                   "_" + color.lower() + "_xl_" + str(i) +
                                   "?$product_image_main_thumbnail")

                products.add_value('image_urls', "http://i1.adis.ws/i/"
                                   "boohooamplience/" +
                                   product_id.lower() +
                                   "_" + color.lower() + "_xl_" + str(i) +
                                   "?$product_image_main")

    def get_name(self, response):
        name = "//div/div[@class='product-col-2 product-detail']/h1/text()"

        return response.xpath(name).extract_first()

    def get_product_id(self, response):
        product_id = "//div/@data-product-details-amplience"

        product_id = response.xpath(product_id).extract_first()
        product_id = product_id.split(',')[0].split(':')[1]
        product_id = product_id.strip('""')

        return product_id

    def get_product_desc(self, response):
        product_desc = "//li[@id='product-short-description-tab']/div/p/text()"
        return response.xpath(product_desc).extract()

    def get_product_care(self, response):
        product_care = "//ul/li[@id='product-custom-composition-tab']/" \
                       "div/text()"
        return response.xpath(product_care).extract()

    def get_colors(self, response):
        colors = "//ul/li[1]/div[2]/ul/li[1]/span/@title"
        return response.xpath(colors).extract()

    def get_product_price(self, response):
        product_price = "//div[@class='product-price']/span/text()"
        return response.xpath(product_price).extract_first()

    def get_alternate_links(self, response):
        alternate_links = "//link[@rel='alternate']/@href"
        return response.xpath(alternate_links).extract()

    def get_alternate_languages(self, response):
        alternate_languages = "//link[@rel='alternate']/@hreflang"
        return response.xpath(alternate_languages).extract()
