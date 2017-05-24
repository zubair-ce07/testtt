from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from OspraySpider.items import OrsayspiderItem
from scrapy import Request


class OrsaySpider(CrawlSpider):
    name = "osray"
    allowed_domains = ["orsay.com"]
    start_urls = ["http://www.orsay.com/de-de"]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('li.level1 > a',)), follow=True),
        Rule(LinkExtractor(allow=(), restrict_css=('ul.products-list > li.item > article > div > a',)),
             callback="parse_items")
    )

    def parse_items(self, response):
        item = OrsayspiderItem()
        item.setdefault('brand', 'Osray')
        item.setdefault('gender', 'female')
        item.setdefault('category', [])
        item['care'] = self.get_care(response)
        item['description'] = [self.get_description(response)]
        item['image_urls'] = [self.get_image(response)]
        item['name'] = [self.get_product_name(response)]
        item['retailer_sku'] = self.get_sku_id(response)[:-2]
        item['skus'] = self.get_skus(response)
        item['url'] = response.url
        item['url_original'] = response.url
        links = self.get_color_url_list(response)
        if links:
            request = Request(links[0], callback=self.parse_additional_colors)
            request.meta['item'] = item
            request.meta['links'] = links[1:]
            return request
        else:
            return item

    def parse_additional_colors(self, response):
        links = response.meta['links']
        item = response.meta['item']
        item['skus'].update(self.get_skus(response))
        item['image_urls'].append(self.get_image(response))
        if links:
            request = Request(links[0], callback=self.parse_additional_colors)
            request.meta['item'] = item
            request.meta['links'] = links[1:]
            return request
        else:
            return item

    def get_skus(self, response):
        sku_id = self.get_sku_id(response)
        sizes = self.get_sizes(response)
        price = self.get_price(response)
        currency_codes = {'$': 'DOL', '€': 'EUR', '£': 'POU'}
        currency = currency_codes[price[-1]]
        price_literals = ""
        result = {}
        for letter in price:
            if letter.isdigit():
                price_literals += letter
        color = self.get_current_color(response)
        for size in sizes:
            stock_info = {}
            formatted_size = size.strip('Unavailable-')
            if 'Unavailable' in size:
                stock_info.update({'out_of_stock': True})
            sku_size_identifier = '{0}_{1}'.format(sku_id, formatted_size)
            result[sku_size_identifier] = {
                'colour': color,
                'currency': currency,
                'price': int(price_literals),
                'size': formatted_size
            }
            result[sku_size_identifier].update(stock_info)
        return result

    def get_care(self, response):
        return [care for care in
                response.css('p.material::text, ul.caresymbols > li > img::attr(src)').extract()]

    def get_description(self, response):
        return response.css('p.description::text').extract_first().strip()

    def get_image(self, response):
        return response.css('#mainZoom::attr(href)').extract_first()

    def get_colors(self, response):
        return response.css('ul.product-colors>li>a>img::attr(title) ').extract()

    def get_current_color(self, response):
        return response.css('ul.product-colors>li>a>img::attr(title) ').extract_first()

    def get_color_url_list(self, response):
        return response.css('ul.product-colors>li>a[href^="http"]::attr(href)').extract()

    def get_sku_id(self, response):
        return response.css('#sku::attr(value)').extract_first()

    def get_product_name(self, response):
        return response.css('h1.product-name::text').extract_first()

    def get_price(self, response):
        return response.css('div.price-box span.price::text').extract_first().strip()

    def get_sizes(self, response):
        unavailable_sizes = []
        for un_size in response.css('div.sizebox-wrapper > ul > li.size-box.size-unavailable::text').extract():
            un_size = un_size.strip()
            if un_size:
                unavailable_sizes.append(un_size)
        sizes = []
        for size in response.css('div.sizebox-wrapper > ul > li::text').extract():
            size = size.strip()
            if size:
                sizes.append('Unavailable-{}'.format(size) if size in unavailable_sizes else size)
        return sizes
