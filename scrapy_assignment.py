# -*- coding: utf-8 -*-
import scrapy


class QuoteSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['http://www.orsay.com/de-de/']

    def collect_product_data(self, response):
        quotes = response.css('div.page')
        Brand = quotes.css('a.logo img::attr(alt)').extract_first()
        Brand = Brand.split(' ')
        Brand = Brand[0]
        Care = quotes.css('p.material::text, li > img::attr(src)').extract()
        Description = quotes.css('div.short-description::text').extract()
        Description = self.skip_spaces(Description)
        Gender = ('Women')
        image_urls = quotes.css('a.MagicZoom::attr(href)').extract()
        product_Name = quotes.css('h1.product-name::text').extract()
        product_id = quotes.css('div.langswitch '
                                'li.store-hu_HU a::attr(href)').extract()
        product_id = product_id[0].split('.html')
        product_id = product_id[0].split('-')
        product_id = product_id[len(product_id) - 1]
        retailer_sku = (product_id[:6])
        size_available = (quotes.css('li[class$="size-box '
                                    'ship-available"]::text').extract())
        size_unAvailable = (quotes.css('li.size-box.ship-available.'
                                      'size-unavailable::text').extract())
        size_available = map(str, size_available)
        size_unAvailable = map(str, size_unAvailable)
        size_available, size_unAvailable = self.skip_character(size_available,
                                                        size_unAvailable)
        Color = quotes.css('img.has-tip::attr(title)').extract()
        Price = quotes.css('span.price::text').extract_first()
        Price = (Price.strip())
        Price = Price.split(' ')
        skus = self.product(size_available,
                                           size_unAvailable,
                                           Color, Price, product_id)
        url = quotes.css('div.langswitch li.store-hu_HU'
                         ' a::attr(href)').extract()
        url = url[0].split('?')
        url = url[0]
        item = {
            'brand': Brand,
            'care': Care,
            'description': Description,
            'gender': Gender,
            'image_url': image_urls,
            'Product_Name': str(product_Name),
            'retailer_sku': retailer_sku,
            'skus': skus,
            'url': url,
        }
        yield item

    def parse(self, response):
        for href in response.css('div.nav-container '
                                 'li.level0 a.level-top::attr(href)'):
            url = href.extract()
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        for href in response.css('div.page '
                                 '.category-products a::attr(href)'):
            url = href.extract()
            yield scrapy.Request(url, callback=self.collect_product_data)
        next_page_url = response.css('li.arrow '
                                     'a.next::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url,
                             callback=self.parse_detail)

    def skip_character(self, size_avail, size_unavail):
        list = []
        list1 = []
        for i in range(len(size_unavail)):
            size = size_unavail[i].strip()
            if size is not '':
                list.append(size)
        for i in range(len(size_avail)):
            size = size_avail[i].strip()
            if size is not '':
                list1.append(size)
        return (list1, list)

    def skip_spaces(self, attribute):
        attr = []
        for space in range(len(attribute)):
            attr1 = attribute[space].strip()
            attr.append(attr1)
        return attr

    def product(self, size_Available,
                               sizeun_Available, Color, Price, product_id):
        skus = []
        for i in range(len(size_Available)):
            skus.append(product_id + '_' + size_Available[i])
            list = []
            Color = 'color: {}'.format(Color)
            list.append(Color)
            Price = 'price: {}'.format(Price)
            list.append(Price)
            list.append('Currency: {}'.format("EUR"))
            size = ('size: {}'.format(size_Available[i]))
            list.append(size)
            skus.append(list)
        for i in range(len(sizeun_Available)):
            skus.append(product_id + '_' + sizeun_Available[i])
            list = []
            Color = 'color: {}'.format(Color)
            list.append(Color)
            Price = 'price: {}'.format(Price)
            list.append(Price)
            list.append('Currency: {}'.format("EUR"))
            size = ('size: {}'.format(sizeun_Available[i]))
            list.append(size)
            list.append("out-of-stock: True")
            skus.append(list)
        return skus

