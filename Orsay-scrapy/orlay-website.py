import scrapy
import json
from orlay.items import SizeInfo, OrlayItem


class OrlayCrawler(scrapy.Spider):
    """This crawler crawls orslay website and extracts all the information from the website"""
    name = 'Orlay'
    start_urls = ['http://www.orsay.com']

    def parse(self, response):
        """This function will get response of Orsay.com and extract all of its categories links to parse again"""

        # Getting links of all the categories, we need only first four of them, last category is redundant
        categories_urls = response.css("ul.level-1 li.level-1 a.has-sub-menu::attr(href)").extract()[:4]

        # Making requests over categories
        for url in categories_urls:
            yield scrapy.Request(url=url, callback=self.parse_categories)

    def parse_categories(self, response):
        """This method takes response of each category and iterate over all the products present in a category"""

        total_products_count = int(
            response.css('div.pagination-product-count.js-pagination-product-count::attr(data-count)').extract_first()
        )

        # Each request generates 72 item records so we have to iterate over all products
        for count in range(0, total_products_count, 72):
            yield scrapy.Request(url=response.url + f"?start={count}&format=page-element",
                                 callback=self.parse_products)

    def parse_products(self, response):
        """It gets response of product list page and then it has to iterate over each single product"""

        # Extracting links of all the products
        product_urls = response.css('ul li div.product-image>a::attr(href)').extract()

        # Iterating over each product
        for product_url in product_urls:
            yield scrapy.Request(url=self.start_urls[0] + product_url, callback=self.get_product_details)

    def get_product_details(self, response):
        """
        This function will extract information of products, it takes response of product page and besides
        extracting info it also traverses onto different pages associated with the product sizes
        """

        item = OrlayItem({
            'title': self.get_title(response),
            'price': self.get_price(response),
            'currency': self.get_currency(response),
            'categories': self.get_category(response),
            'care': self.get_care(response),
            'details': self.get_detail(response),
            'images': self.get_images(response),
            'item_url': response.url,
            'sizes': self.get_sizes(response),
            'out_of_stock_products': self.get_out_of_stock_products(response),
            'retail_sku': self.get_retail_sku(response),
            'skus': {},
        })

        # Extracting available sizes and related links of products
        size_and_url = self.get_sizes_and_links_of_product(response)

        # If sizes are available, traverse over those size urls, else return item
        if len(size_and_url) > 0:
            yield self.create_size_page_request(size_and_url, item)

        else:
            yield item

    def create_size_page_request(self, size_and_url, item):
        """This function takes urls of iszes and item of product data to create a scrapy Request according to them"""
        size_key, size_url = size_and_url.popitem()
        request = scrapy.Request(url=size_url + '&Quantity=1&format=ajax&productlistid=undefined',
                                 callback=self.parse_sizes)

        # Appending data in request to pass onto next function
        request.meta['item_data'] = item
        request.meta['sizes_to_traverse'] = size_and_url
        request.meta['current_size'] = size_key

        return request

    def parse_sizes(self, response):
        """This function takes response of size-info-page and stores the information in respective item object"""
        item_data = response.meta['item_data']
        current_size = response.meta['current_size']
        urls_of_sizes = response.meta['sizes_to_traverse']

        item_data['skus'][current_size] = self.get_size_info(response)

        if len(urls_of_sizes) > 0:
            yield self.create_size_page_request(urls_of_sizes, item_data)
        else:
            yield item_data

    def get_size_info(self, response):
        """takes response of product sizes page and return information in the form of SizeInfo object"""

        # Extracting details
        data = response.css('div.js-product-content-gtm::attr(data-product-details)').extract_first()

        # Converting string dict into json to parse it
        data_json = json.loads(data)

        # Creating object of information
        size_info = SizeInfo({
            'price': data_json['grossPrice'],
            'currency': data_json['currency_code'],
            'colors': data_json['color'],
            'size': data_json['size'],
        })

        return size_info

    def convert_lists_to_dict(self, sizes, links):
        """converts two lists into one dict"""
        return dict(zip(sizes, links))

    def get_sizes_and_links_of_product(self, response):
        """It takes product page response and returns sizes and their links in the form of dict"""

        sizes_of_product = [size.replace('\n', '') for size in
                            response.css('ul.swatches.size>li.selectable a::text').extract()]
        links_of_product = response.css('ul.swatches.size>li.selectable a::attr(href)').extract()

        return self.convert_lists_to_dict(sizes_of_product, links_of_product)

    def get_title(self, response):
        """Extracts and returns Title of product"""
        return response.css('h1.product-name::text').extract_first()

    def get_price(self, response):
        """Extracts and returns Price of product"""
        return response.css('div.product-price span::text').extract_first().replace('\n', '').split(' ')[0]

    def get_currency(self, response):
        """Extracts and returns Currency of product"""
        return response.css('div.locale-item.current span.country-currency::text').extract_first()

    def get_category(self, response):
        """Extracts and returns Category of product"""
        return response.css('a.breadcrumb-element-link span::text').extract()

    def get_care(self, response):
        """Extracts and returns Care of product"""
        return response.css('div.product-info-block p::text').extract_first()

    def get_detail(self, response):
        """Extracts and returns Details of product"""
        return response.css('div.product-details>div>div::text').extract()[1:]

    def get_images(self, response):
        """Extracts and returns Images of product"""
        response.css('img.productthumbnail::attr(src)').extract()

    def get_sizes(self, response):
        """Extracts and returns Available Sizes of product"""
        return [size.replace('\n', '') for size in response.css('ul.swatches.size>li.selectable a::text').extract()]

    def get_out_of_stock_products(self, response):
        """Extracts and returns the products which are out of stock"""
        return [size.replace('\n', '') for size in response.css('ul.swatches.size>li.unselectable a::text').extract()]

    def get_retail_sku(self, response):
        """Extracts and returns Retail-Sku of product"""
        return response.css('input.js-product-id::attr(value)').extract_first()
