# -*- coding: utf-8 -*-
import scrapy


class QuoteSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['http://www.orsay.com/de-de/']

    def collect_product_data(self, response):
        quotes = response.css('div.page')
        brand = quotes.css('a.logo img::attr(alt)').extract_first()
        brand = (brand.split(' '))[0]
        care = quotes.css('p.material::text, li > img::attr(src)').extract()
        description = quotes.css('div.short-description::text').extract()
        description = self.clean_spaces(description)
        gender = ('Women')
        image_urls = quotes.css('a.MagicZoom::attr(href)').extract()
        product_name = quotes.css('h1.product-name::text').extract()
        id = quotes.css('li.store-hu_HU a::attr(href)').extract()
        id, retailer_sku = self.product_id(id)
        size_available = (quotes.css('li[class$="size-box '
                                    'ship-available"]::text').extract())
        size_unAvailable = (quotes.css('li.size-box.ship-available.'
                                      'size-unavailable::text').extract())
        size_available = map(str, size_available)
        size_unAvailable = map(str, size_unAvailable)
        size_available, size_unAvailable = self.clean_char(size_available,
                                                        size_unAvailable)
        color = quotes.css('img.has-tip::attr(title)').extract()
        price = quotes.css('span.price::text').extract_first()
        price = (price.strip())
        price = price.split(' ')
        skus = self.product_details(size_available,
                                           size_unAvailable,
                                           color, price, id)
        url = quotes.css('li.store-hu_HU'
                         ' a::attr(href)').extract_first()
        url = (url.split('?'))[0]
        product = scrapy.Field(brand=brand, care=care,
                               description=description, gender=gender,
                               image_url=image_urls, name=product_name,
                               retailer_sku=retailer_sku, skus=skus,
                               url=url, origional_url=url)
        yield product

    def product_id(self, id):
        id = id[0].split('.html')
        id = id[0].split('-')
        id = id[len(id) - 1]
        retailer_sku = (id[:6])
        return(id, retailer_sku)

    def parse(self, response):
        for href in response.css('li.level0 '
                                 'a.level-top::attr(href)').extract():
            yield scrapy.Request(url=href, callback=self.parse_next_urls)

    def parse_next_urls(self, response):
        for href in response.css('.category-products a::attr(href)').extract():
            yield scrapy.Request(href, callback=self.collect_product_data)
        next_page_url = response.css('li.arrow '
                                     'a.next::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url,
                             callback=self.parse_next_urls)

    def clean_char(self, size_avail, size_unavail):
        avaiable = []
        un_avaiable = []
        for i in range(len(size_unavail)):
            size = size_unavail[i].strip()
            if size is not '':
                un_avaiable.append(size)
        for i in range(len(size_avail)):
            size = size_avail[i].strip()
            if size is not '':
                avaiable.append(size)
        return (avaiable, un_avaiable)

    def clean_spaces(self, attribute):
        attr = []
        for space in range(len(attribute)):
            attr1 = attribute[space].strip()
            attr.append(attr1)
        return attr

    def product_details(self, size_available,
                               sizeun_available, colors, prices, product_id):
        data = []
        for i in range(len(size_available)):
            id_size = '{}_{}'.format(product_id, size_available[i])
            product_info_available = scrapy.Field(color=colors,
                                                   price=prices[0],
                                                   currency="EUR",
                                                   size=size_available[i])
            sku1 = (id_size, product_info_available)
            data.append(sku1)
        for i in range(len(sizeun_available)):
            id_size = '{}_{}'.format(product_id, sizeun_available[i])
            product_info_available = scrapy.Field(color=colors,
                                                  price=prices[0],
                                                  currency="EUR",
                                                  size=sizeun_available[i],
                                                  out_of_stock=True)
            sku2 = (id_size, product_info_available)
            data.append(sku2)
        skus = scrapy.Field(sku=data)
        return skus

