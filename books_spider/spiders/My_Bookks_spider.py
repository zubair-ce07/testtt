# -*- coding: utf-8 -*-
import scrapy
import re
from books_spider.items import BookItemLoader, BooksSpiderItem


class MyBookksSpider(scrapy.Spider):
    name = 'My_Books_spider'
    allowed_domains = ['kaymu.pk']
    start_urls = ['http://www.kaymu.pk/books/']
    next_page_handler = 0

    def parse(self, response):
        for books_div in response.xpath('//div[@class="small-3 productItem no-shrink mvs"]'
                                        '/article/a/@href').extract():
            books_div = response.urljoin(books_div)
            yield scrapy.Request(books_div, callback=self.get_items_details)
        if self.next_page_handler < 3:
            next_page = response.xpath('//*[@id="kaymu"]/div[4]/div[2]/div/div/a[6]/@href').extract_first()
        elif self.next_page_handler == 29:
            next_page = response.xpath('//*[@id="kaymu"]/div[4]/div[2]/div/div/a[6]/@href').extract_first()
        elif self.next_page_handler == 3:
            next_page = response.xpath('//*[@id="kaymu"]/div[4]/div[2]/div/div/a[7]/@href').extract_first()
        else:
            next_page = response.xpath('//*[@id="kaymu"]/div[4]/div[2]/div/div/a[8]/@href').extract_first()
        if next_page is not None:
            # print(next_page)
            next_page1 = response.urljoin(next_page)

            self.next_page_handler += 1
            print(self.next_page_handler)
            print(next_page1)
            yield scrapy.Request(next_page1, callback=self.parse)

    def get_items_details(self, response):
        books_items = BooksSpiderItem()
        # book_item_loader = BookItemLoader(item=BooksSpiderItem(), response=response)
        book_price_holder = response.xpath('//span[@class="discount-price price fsize-24 bold"]'
                                           '/text()').extract_first()
        if book_price_holder is None:
            book_price_holder = response.xpath('//div[@class="no-discount price fsize-24 bold"]'
                                               '/text()').extract_first(default='not-found')

        # book_item_loader.add_value('Book_Name', response.xpath('//h1[@class="s-bold fsize-16 man"]
        # /text()').extract_first())
        # book_item_loader.add_value('Book_price', book_price_holder)
        # book_item_loader.add_value('Book_Category', response.xpath('//ul[@class="breadcrumbs"]/li[4]/a
        # /text()')..extract_first())
        # book_item_loader.add_value('Book_Author', response.xpath('//div[@class="hr row"]/div[1]/span
        # /text()').extract_first())
        # book_item_loader.add_value('Book_Condition', response.xpath('//div[@class="hr row"]/div[3]/span
        # /text()').extract_first())
        # book_item_loader.add_value('Book_Language', response.xpath('//div[@class="hr row"]/div[4]/span
        # /text()').extract_first())
        # book_item_loader.add_value('Book_Weight', response.xpath('//div[@class="hr row"]/div[5]/span
        # /text()').extract_first())
        # book_item_loader.add_value('Image__Img_Url', response.xpath('//*[@id="pdp-info"]'
        #                                                             '/div[1]/div/div[3]/div/div/div/img/@data-layzr').extract_first())
        # return book_item_loader.load_item()
        # selector.xpath('//a[contains(@href, "image")]/text()').re(r'Name:\s*(.*)')

        books_items['Book_Name'] = response.xpath('//h1[@class="s-bold fsize-16 man"]'
                                                  '/text()').extract_first(default='not-found')
        temp_var = re.findall(r'\d+', book_price_holder)
        books_items['Book_price'] = temp_var[-1]
        books_items['Book_Category'] = response.xpath('//ul[@class="breadcrumbs"]/li[4]/a'
                                                      '/text()').extract_first(default='not-found')
        books_items['Book_Author'] = response.xpath('//div[@class="hr row"]/div[1]/span/'
                                                    'text()').extract_first(default='not-found')
        books_items['Book_Condition'] = response.xpath('//div[@class="hr row"]/div[3]/span'
                                                       '/text()').extract_first(default='not-found')
        books_items['Book_Language'] = response.xpath('//div[@class="hr row"]/div[4]/span'
                                                      '/text()').extract_first(default='not-found')
        books_items['Book_Weight'] = response.xpath('//div[@class="hr row"]/div[5]/span'
                                                    '/text()').extract_first(default='not-found')
        books_items['Image__Img_Url'] = response.xpath('//div[@class="img vh-center auto-h zoom"]'
                                                       '/img/@data-layzr').extract_first(default='not-found')
        return books_items
