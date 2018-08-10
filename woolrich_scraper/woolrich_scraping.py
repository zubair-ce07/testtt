import scrapy
from scrapy.linkextractors import LinkExtractor


class WoolRich(scrapy.Spider):
    """This class contains small helper classes as well as
    other two main classes which iterate through all the products
    in the entire site"""

    name = "WoolRich_Spider"
    allowed_domains = ['woolrich.com']
    start_urls = ['https://www.woolrich.com/men/?sort=featured&page=1']

    def get_product_name(self, response):
        """This helper function fetches the name of the product"""
        name = {
            'Product Name': response.css('h1.productView-title::text').extract()
        }
        return name

    def get_product_style(self, response):
        """This helper function fetches the product style"""
        style = {
            'Style': response.css('.productView-product > div:nth-child(2) >'
                                  ' strong:nth-child(1)::text').extract()
        }
        return style

    def get_product_price(self, response):
        """This helper function fetches the product price"""
        price = {
            'Price': response.css('span.price::text')[0].extract()
        }
        return price

    def get_product_size(self, response):
        """This helper function fetches the product size"""
        size = {
            'Size': response.css('span.form-option-variant::text').extract()
        }
        return size

    def get_product_features(self, response):
        """This helper function fethches the product features"""
        features = {
            'Features': response.css('#features-content > li::text').extract()
        }
        return features

    def get_product_description(self, response):
        """This helper function fetches the product description"""
        description = {
            'Descrption': response.css('#details-content::text').extract()
        }
        return description

    def get_product_path(self, response):
        """This helper function fetches the product path from home
        in the website"""
        path = {
            'Path': response.css('a.breadcrumb-label::text').extract()
        }
        return path

    def get_product_image(self, response):
        """This helper function fetches all the links of the product images"""
        images = {
            'Images': response.css('div.zoom> a::attr(data-zoom-image)').extract()
        }
        return images

    def get_product_color(self, response):
        """This helper function fetches all product colors available"""
        color_unsorted = response.css('label.form-option-swatch> '
                                      'span::attr(title)').extract()
        while 'Loading...' in color_unsorted:
            color_unsorted.remove('Loading...')
        color = {
            'Colors': color_unsorted
        }
        return color

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

        final_dict = {
            **self.get_product_name(response),
            **self.get_product_color(response),
            **self.get_product_price(response),
            **self.get_product_size(response),
            **self.get_product_style(response),
            **self.get_product_path(response),
            **self.get_product_image(response),
            **self.get_product_features(response),
            **self.get_product_description(response)
        }
        yield final_dict
