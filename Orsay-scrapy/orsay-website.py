import json
from scrapy import Request
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from orsay.items import SizeInfo, OrsayItem


class OrsayCrawler(CrawlSpider):
    """This crawler crawls orsay website and extracts all the information from the website"""
    name = 'Orsay'
    allowed_domains = ["orsay.com"]
    start_urls = ['http://www.orsay.com']

    rules = (
        Rule(LinkExtractor(restrict_css="nav.header-navigation>ul>li:nth-child(2) a.level-1"),
             callback='parse_categories'),
        Rule(LinkExtractor(restrict_css=".product-swatch-item"), callback='parse_products')
    )

    def parse_categories(self, response):
        """This method takes response of each category and iterate over all the products
         present in a category
        """

        total_products_count = self.get_product_count(response)

        for count in range(0, total_products_count, 72):
            yield Request(url=f"{response.url}?start={count}&format=page-element")

    def parse_products(self, response):
        """This function will extract information of products,it takes response of product page
        and besides extracting info it also traverses onto different pages associated with the
        product sizes
        """

        item = OrsayItem()
        item['brand'] = 'Orsay'
        item['gender'] = 'women'
        item['name'] = self.get_title(response)
        item['category'] = self.get_category(response)
        item['care'] = self.get_care(response)
        item['description'] = self.get_detail(response)
        item['image_urls'] = self.get_images(response)
        item['url'] = response.url
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['skus'] = {}

        unavailable_products = self.get_out_of_stock_products(response)
        self.populate_out_of_stock_products(unavailable_products, item)

        sizes_and_urls = self.get_sizes_and_links_of_product(response)

        if len(sizes_and_urls) > 0:
            current_size, size_url = sizes_and_urls.popitem()
            request = Request(url=size_url + '&Quantity=1&format=ajax&productlistid=undefined',
                              callback=self.parse_sizes)
            request.meta['size_data'] = item, sizes_and_urls, current_size
            yield request
        else:
            yield item

    def parse_sizes(self, response):
        """This function takes response of size-info-page and stores the information in
         respective item object
        """

        item_data, urls_of_sizes, current_size = response.meta.get('size_data')
        skus = item_data.get('skus')
        skus[item_data.get('retailer_sku') + '_' + str(current_size)] = self.get_size_info(response)

        if len(urls_of_sizes) > 0:
            current_size, size_url = urls_of_sizes.popitem()
            request = Request(url=size_url + '&Quantity=1&format=ajax&productlistid=undefined',
                              callback=self.parse_sizes)
            request.meta['size_data'] = item_data, urls_of_sizes, current_size
            yield request
        else:
            yield item_data

    def populate_out_of_stock_products(self, unavailable_products, item):
        """This function populates informationabout products which are not in stock"""

        for product_size in unavailable_products:
            sku = SizeInfo()
            sku['out_of_stock'] = True
            sku['size'] = str(product_size)
            item.get('skus')[item.get('retailer_sku') + '_' + str(product_size)] = sku

    def get_size_info(self, response):
        """Takes response of product sizes page and return information in the form of
        SizeInfo object
        """

        data = response.css('div.js-product-content-gtm::attr(data-product-details)').extract_first()

        data_json = json.loads(data)

        size_info = SizeInfo({
            'out_of_stock': False,
            'price': data_json.get('grossPrice'),
            'currency': data_json.get('currency_code'),
            'colour': data_json.get('color'),
            'size': data_json.get('size'),
        })

        return size_info

    def get_sizes_and_links_of_product(self, response):
        """It takes product page response and returns sizes and their links in the form of dict"""

        size_tags = response.css('ul.swatches.size>li.selectable a::text').extract()
        sizes_of_product = []
        for size in size_tags:
            sizes_of_product.append(size.replace('\n', ''))

        links_of_product = response.css('ul.swatches.size>li.selectable a::attr(href)').extract()

        return dict(zip(sizes_of_product, links_of_product))

    def get_title(self, response):
        """Extracts and returns Title of product"""

        return response.css('h1.product-name::text').extract_first()

    def get_price(self, response):
        """Extracts and returns Price of product"""

        price_tag = response.css('div.product-price span::text').extract_first()
        try:
            price = price_tag.replace('\n', '').split(' ')[0]
        except IndexError:
            price = 0
        return price

    def get_currency(self, response):
        """Extracts and returns Currency of product"""

        return response.css('span.country-currency::text').extract_first()

    def get_category(self, response):
        """Extracts and returns Category of product"""

        return response.css('a.breadcrumb-element-link span::text').extract()

    def get_care(self, response):
        """Extracts and returns Care of product"""

        return response.css('div.product-info-block p::text').extract_first()

    def get_detail(self, response):
        """Extracts and returns Details of product"""

        try:
            description = response.css('div.product-details>div>div::text').extract()[1:]
        except IndexError:
            description = ''

        return description

    def get_images(self, response):
        """Extracts and returns Images of product"""

        return response.css('img.productthumbnail::attr(src)').extract()

    def get_out_of_stock_products(self, response):
        """Extracts and returns the products which are out of stock"""

        size_tags = response.css('ul.swatches.size>li.unselectable a::text').extract()
        product_sizes = []
        for size in size_tags:
            product_sizes.append(size.replace('\n', ''))

        return product_sizes

    def get_retailer_sku(self, response):
        """Extracts and returns Retail-Sku of product"""

        sku = response.css('input.js-product-id::attr(value)').extract_first()
        if not sku:
            sku = response.css('input.js-producrt-id::attr(value)').extract_first()

        return sku if sku else ''

    def get_product_count(self, response):
        """ It returns total number of products present in a specific category"""

        return int(response.css('div.pagination-product-count::attr(data-count)').extract_first())

