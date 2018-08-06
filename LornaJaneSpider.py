import math
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LornajaneSpider(CrawlSpider):
    name = 'LornaJaneSpider'
    allowed_domains = ['lornajane.sg']
    start_urls = ['https://www.lornajane.sg/']
    download_delay = 3

    rules = (
        Rule(LinkExtractor(restrict_css='.main-menu li:nth-child(1) a:nth-child(1)'),
             callback='parse_main_products'),
    )

    def parse_main_products(self, response):
        product_links = self.get_sub_prod_links(response)
        for product in product_links:
            yield scrapy.http.Request(product, callback=self.parse_products)

        no_of_records = self.records_for_category(response)
        no_of_records = int(no_of_records[-1])
        max_pages = int(math.ceil(no_of_records / 20.0))

        for next_page in range(1, max_pages):
            yield scrapy.http.Request(self.next_page_link(next_page, response), callback=self.parse_main_products)

    def parse_products(self, response):
        item = {
            'care': self.care(response),
            'description': self.description(response),
            'type': self.product_type(response),
            'image_url': self.image_url(response),
            'product_name': self.product_name(response),
            'sku': self.sku_id(response),
            'url': response.url,
            'skus': self.populate_sku_for_all_sizes(response)
        }

        color_links = self.color_links(response)
        if color_links:
            yield scrapy.http.Request(color_links.pop(0), callback=self.parse_colors,
                                      meta={'color_links': color_links, 'item': item})
        else:
            yield item

    def parse_colors(self, response):
        color_links = response.meta['color_links']
        item = response.meta['item']
        item['image_url'] += self.image_url(response)
        item['skus'].update(self.populate_sku_for_all_sizes(response))

        if color_links:
            yield scrapy.http.Request(color_links.pop(0), callback=self.parse_colors,
                                      meta={'color_links': color_links, 'item': item})
        else:
            yield item

    def populate_sku_for_all_sizes(self, response):
        skus = {}
        sku_id = self.sku_id(response)
        for idx, size in enumerate(self.size_color(response)['size']):
            values = {
                'color': self.color(response),
                'currency': self.currency(response),
                'price': self.price(response),
                'stock': self.stock(idx, self.size_color(response)['stock']),
                'size': size
            }
            skus['{0}_{1}'.format(sku_id, size)] = values
        return skus

    def next_page_link(self, next_page, response):
        return '{0}?page={1}'.format(response.url.split('?')[0], next_page)

    def image_url(self, response):
        return response.urljoin(response.css('.product-slider-image .item picture source::'
                                             'attr(srcset)').extract_first())

    def stock(self, idx, stock_list):
        return 'Out of Stock' if 'disabled' in stock_list[idx] else 'In Stock'

    def records_for_category(self, response):
        return response.css('.count-text::text').extract()[1].split(' ')

    def get_sub_prod_links(self, response):
        prod = LinkExtractor(restrict_css='.product-item .product-grid-item div:nth-child(1) '
                                          ' a:nth-child(1)', strip=True).extract_links(response)
        return [p.url for p in prod]

    def color_links(self, response):
        prod = LinkExtractor(restrict_css='.color-swatch ul:nth-child(1) li a:not(.selected)', attrs='data-url'
                             ).extract_links(response)
        return [p.url for p in prod]

    def size_color(self, response):
        sz_selector = response.css('#sizeWrap a')
        col_size = {
            'stock': [],
            'size': []
        }
        for resp in sz_selector:
            col_size['stock'].append(resp.css('a::attr(class)').extract_first().strip())
            col_size['size'].append(resp.css('a::text ').extract_first().strip())
        return col_size

    def product_name(self, response):
        return response.css('.pro-heading-sec h1:nth-child(3)::text').extract()[0]

    def color(self, response):
        return response.css('.selected span::attr(title)').extract()[0].encode('utf-8')

    def product_type(self, response):
        return response.css('.breadcrumb ul:nth-child(1) li:nth-child(3) a:nth-child(1)::'
                            'text').extract()[0].strip()

    def gender(self, response):
        return response.css('female').extract()[0]

    def price(self, response):
        return response.css('.price:nth-child(4)::text').extract()[1]

    def description(self, response):
        desc = response.css('#desc1 .mobile_toggle div p:nth-child(3)::text').extract()
        if not desc:
            desc = response.css('#desc1 .mobile_toggle div p:nth-child(2)::text').extract()
        return desc[0]

    def care(self, response):
        return response.css('.mobile_toggle:nth-child(1) ul:nth-child(6) li::text').extract()

    def sku_id(self, response):
        return response.css('.mobile_toggle:nth-child(1) p:nth-child(1)::text').extract()[0].split(':')[1]

    def currency(self, response):
        return response.css('.price:nth-child(4) span:nth-child(1)::text').extract()[0]

