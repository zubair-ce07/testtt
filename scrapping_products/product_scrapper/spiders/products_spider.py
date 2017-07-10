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

        product_by_category = "div.nav-wrapper > ul.menu-vertical " \
                              "> li > a::attr('href')"
        categorized_product_links = response.css(product_by_category)

        categorized_product_links = categorized_product_links.extract()

        for link in categorized_product_links:
            yield scrapy.Request(url=link, meta={'products_to_retrieve': 0},
                                 callback=self.get_products)

    def get_products(self, response):
        products_to_retrieve = response.meta['products_to_retrieve']

        product = "div.search-result-content > ul > li > div >" \
                  " div:nth-child(1) > a::attr('href')"
        product_links = response.css(product).extract()

        for link in product_links:
            complete_link = urljoin(response.url, link)
            yield scrapy.Request(url=complete_link,
                                 callback=self.retrieve_product_info)

            products_to_retrieve += 1
            if products_to_retrieve >= self.no_of_products:
                return

        # moving onto the next page
        next_page = "ul.pagination-list li.pagination-item-next a"
        next_products_page_link = response.css(next_page).extract_first()

        if next_products_page_link:
            yield scrapy.Request(url=next_products_page_link,
                                 meta={'products_to_retrieve':
                                       products_to_retrieve},
                                 callback=self.get_products)

    def retrieve_product_info(self, response):
        name_css = ".product-detail h1.product-name::text"

        product_id_css = "div#product-content div.product-number span::text"

        product_desc_css = "li#product-short-description-tab > div > p::text"

        product_care_css = "ul > li#product-custom-composition-tab > div::text"

        product_price_css = "div.product-price > span::text"
        url = response.url

        product_id = response.css(product_id_css).extract_first()

        product = ItemLoader(item=ProductScrapperItem(), response=response)
        product.add_css('name', name_css)
        product.add_css('product_desc', product_desc_css)
        product.add_css('product_price', product_price_css)
        product.add_css('product_care', product_care_css)
        product.add_value('url', url)
        product.add_value('product_id', product_id)

        colors = self.get_colors(response)
        self.add_image_links(product, colors, product_id)

        language_id = 0
        alternate_links = self.get_alternate_links(response)
        for link in alternate_links:
            language = self.get_alternate_languages(response)
            yield scrapy.Request(url=link,
                                 meta={
                                       'product': product,
                                       'language': language[language_id],
                                       'colors': colors
                                       },
                                 callback=self.generate_skus)
            language_id += 1

    def generate_skus(self, response):
        product_price_css = "div.product-price > span::text"
        product_price = response.css(product_price_css).extract_first()

        colors = self.get_colors(response)

        product = response.meta['product']
        language = response.meta['language']
        colors = response.meta['colors']

        skus = {}
        skus[language] = {}
        skus[language]['price'] = product_price
        skus[language]['colors'] = []
        for color in colors:
            skus[language]['colors'].append(color.split(':')[1].strip(' '))

        product.add_value('skus', skus)

        return product.load_item()

    def add_image_links(self, product, colors, product_id):
        for color in colors:
            color = color.split(':')[1].strip(' ')

            image_template = "http://i1.adis.ws/i/boohooamplience/" \
                             "{id}_{color}_xl?$product_image_main_thumbnail"

            image_url = image_template.format(id=product_id.lower(),
                                              color=color.lower())
            product.add_value('image_urls', image_url)

            image_template = "http://i1.adis.ws/i/boohooamplience/" \
                             "{id}_{color}_xl_{img_no}" \
                             "?$product_image_main_thumbnail"

            for i in range(1, 4):
                image_url = image_template.format(id=product_id.lower(),
                                                  color=color.lower(),
                                                  img_no=str(i))
                product.add_value('image_urls', image_url)

    def get_colors(self, response):
        colors_css = "ul > li:nth-child(1) > div:nth-child(2) > ul >" \
                     "li:nth-child(1) > span::attr('title')"
        return response.css(colors_css).extract()

    def get_alternate_links(self, response):
        alternate_links_css = "head > link[rel='alternate']::attr('href')"
        return response.css(alternate_links_css).extract()

    def get_alternate_languages(self, response):
        alternate_languages_css = "head > link[rel='alternate']" \
                                  "::attr('hreflang')"
        return response.css(alternate_languages_css).extract()
