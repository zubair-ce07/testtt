from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from softsurroundings_crawler.items import SoftSurroundingsCrawlerItem, ProductLoader


class SoftSurroundingSpider(CrawlSpider):
    name = 'soft_surroundings_spider'
    start_urls = ['https://www.softsurroundings.com/']
    category_css = '.clMn'
    product_css = '.product'

    rules = (
        Rule(LinkExtractor(restrict_css=category_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        product = self.parse_info(response)
        product['requests'] = self.size_requests(response)

        return self.next_request_or_product(product)

    def parse_info(self, response):
        product = ProductLoader(item=SoftSurroundingsCrawlerItem(), response=response)
        product.add_css('pid', 'span[itemprop="productID"]::text')
        product.add_value('gender', 'women')
        product.add_css('category', '.pagingBreadCrumb > a::text')
        product.add_value('brand', 'Soft Surroundings')
        product.add_value('url', response.url)
        product.add_css('name', 'span[itemprop="name"]::text')
        product.add_css('description', '.productInfo::text')
        product.add_css('description', '.productInfo > p::text')
        product.add_css('care', '.tabContent.sel::text')
        product.add_css('image_urls', '.alt_dtl::attr(href)')
        product.add_value('skus', self.skus(response))
        return product.load_item()

    def category_size(self, response):
        size_ids = response.css('#sizecat > a::attr(id)').getall()
        return [size.split('_')[1] for size in size_ids]

    def size_requests(self, response):
        size_ids = self.category_size(response)
        return [response.follow('/p/' + size, callback=self.parse_skus) for size in size_ids]

    def next_request_or_product(self, product):
        if product['requests']:
            request = product['requests'].pop()
            request.meta['product'] = product
            return request
        else:
            del product['requests']

        return product

    def parse_skus(self, response):
        product = response.meta['product']
        product_skus = self.skus(response)
        if product_skus:
            product['skus'].append(product_skus)

        return self.next_request_or_product(product)

    def skus(self, response):
        product_detail = []
        colour_options = response.css('.swatchHover > span::text , .basesize::text').getall()
        size_options = response.css('.box.size::text').getall()

        if colour_options and size_options:
            product_detail = self.color_skus(response, colour_options, size_options)

        elif size_options:
            product_detail = self.size_skus(response, size_options)

        return product_detail

    def color_skus(self, response, colour_options, size_options):
        product_detail = []

        for size in size_options:
            for color in colour_options:
                product = self.product_price_detail(response)
                product['color'] = color
                product['size'] = size
                product['sku_id'] = color + "_" + size

                product_detail.append(product)

        return product_detail

    def size_skus(self, response, size_options):
        product_detail = []
        for size in size_options:
            product = self.product_price_detail(response)
            product['size'] = size
            product['sku_id'] = size

            product_detail.append(product)
        return product_detail

    def product_price_detail(self, response):
        product_price = {
            'price': response.css('span[itemprop="price"]::text').get(),
            'currency': response.css('span[itemprop="priceCurrency"]::attr(content)').get(),
        }

        previous_price = response.css('.ctntPrice::text').get()
        if previous_price:
            product_price['previous_price'] = previous_price

        return product_price

