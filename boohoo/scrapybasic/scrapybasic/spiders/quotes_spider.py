import scrapy


class QuotesSpider(scrapy.Spider):
    name = "boohoo"
    start_urls = [
        'https://www.boohooman.com/',
    ]

    def parse(self, response):
        for item in response.css('li.has-submenu'):
            for subitem in item.css('li a'):
                print(subitem.css('a::attr(href)').extract_first())
                print(subitem.css('a::text').extract_first())
                next_page = subitem.css('a::attr(href)').extract_first()
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse_url)

    def parse_url(self, response):
        for item in response.css('div.product-tile'):
            yield {
                'item': {
                      'name': item.css('div.product-name a::text')
                                  .extract_first(),
                      'imageUrl': response.urljoin(item.css(
                                  'div.product-image a::attr(href)')
                                  .extract_first()),
                      'standardPrice': item.css(
                                       'div.product-pricing \
                                        span.product-standard-price::text')
                                       .extract_first(),
                      'salesPrice': item.css(
                                    'div.product-pricing \
                                     span.product-sales-price::text')
                                     .extract_first()
                }
            }

        next_page = response.css('li.pagination-item a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)




# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         'https://www.boohooman.com/mens/shoes',
#     ]
#
    # def parse(self, response):
    #     for item in response.css('div.product-tile'):
    #         yield {
    #             'item': {
    #                   'name': item.css('div.product-name a::text')
    #                               .extract_first(),
    #                   'imageUrl': response.urljoin(item.css(
    #                               'div.product-image a::attr(href)')
    #                               .extract_first()),
    #                   'standardPrice': item.css(
    #                                    'div.product-pricing \
    #                                     span.product-standard-price::text')
    #                                    .extract_first(),
    #                   'salesPrice': item.css(
    #                                 'div.product-pricing \
    #                                  span.product-sales-price::text')
    #                                  .extract_first()
    #             }
    #         }
    #
    #     next_page = response.css('li.pagination-item a::attr(href)').extract_first()
    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page, callback=self.parse)




# class QuotesSpider(scrapy.Spider):
#     name = "boohoo"
#     start_urls = [
#         'https://www.boohooman.com/mens/shoes',
#     ]
#
#     def parse(self, response):
#         # import pdb; pdb.set_trace()
#         for item in response.css('nav.main-navigation'):
#             link_name = item.css('li.has-submenu a::text').extract()
#             link_url = item.css('li.has-submenu a::attr(href)').extract()
#             for url in link_url:
#                 yield response.follow(url, callback=self.parse_url)
#
#     def parse_url(self, response):
#         # import pdb; pdb.set_trace()
#         print(response)
#             # print(link_name)
#             # print(link_url)
#             # for sub_item in item.css('ul.menu-vertical'):
#             #     sub_link_name = sub_item.css('li a::text').extract_first()
#             #     sub_link_url = sub_item.css('li a::attr(href)').extract_first()
#             #     print(sub_link_name)
#             #     print(sub_link_url)
