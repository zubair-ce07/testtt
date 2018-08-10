import scrapy
from scrapy.linkextractors import LinkExtractor
from woolrich.items import WoolrichItem

class WoolRich(scrapy.Spider):
    """This class contains small helper classes as well as
    other two main classes which iterate through all the products
    in the entire site"""

    name = "woolrich_spider"
    allowed_domains = ['woolrich.com']
    start_urls = ['https://www.woolrich.com/men/?sort=featured&page=1']

    def get_product_name(self, response):
        """This helper function fetches the name of the product"""

        product_name = response.css('h1.productView-title::text').extract()

        return product_name

    def get_product_style(self, response):
        """This helper function fetches the product style"""

        product_style = response.css('.productView-product > div:nth-child(2) > '
                                     'strong:nth-child(1)::text').extract()
        return product_style

    def get_product_price(self, response):
        """This helper function fetches the product price"""

        product_price = response.css('span.price::text')[0].extract()
        return product_price

    def get_product_size(self, response):
        """This helper function fetches the product size"""

        product_size = response.css('span.form-option-variant::text').extract()
        return product_size

    def get_product_features(self, response):
        """This helper function fethches the product features"""

        product_feature = response.css('#features-content > li::text').extract()
        return product_feature

    def get_product_description(self, response):
        """This helper function fetches the product description"""

        product_description = response.css('#details-content::text').extract()
        return product_description

    def get_product_path(self, response):
        """This helper function fetches the product path from home
        in the website"""

        product_path = response.css('a.breadcrumb-label::text').extract()
        return product_path

    def get_product_image(self, response):
        """This helper function fetches all the links of the product images"""

        product_image = response.css('div.zoom> a::attr(data-zoom-image)').extract()
        return product_image

    def get_product_color(self, response):
        """This helper function fetches all product colors available"""
        color_unsorted = response.css('label.form-option-swatch> '
                                      'span::attr(title)').extract()
        while 'Loading...' in color_unsorted:
            color_unsorted.remove('Loading...')
        product_color = color_unsorted
        return product_color

    def parse(self, response):
        """In this method, the program will iterate through the links and then
         call the individual method for further retrieval of details."""
        links = response.css('li.product> article> figure>'
                             ' a::attr(href)').extract()
        for link in links:
            yield scrapy.Request(link,
                                 callback=self.parse_of_clothing_item)

        next_page = LinkExtractor(allow=[''], deny=['sort', 'size',
                                                    'Size', 'fsnf'])
        links = next_page.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,
                                 callback=self.parse)

    def parse_of_clothing_item(self, response):
        """This method crawls through individual pages and gathers all the
        details. The helper functions are called and all their responses
        are appended to a single dictionary"""

        complete_product = WoolrichItem(
            name=self.get_product_name(response),
            color = self.get_product_color(response),
            price = self.get_product_price(response),
            size = self.get_product_size(response),
            style = self.get_product_style(response),
            path = self.get_product_path(response),
            image = self.get_product_image(response),
            features = self.get_product_features(response),
            description = self.get_product_description(response)
        )
        yield complete_product
