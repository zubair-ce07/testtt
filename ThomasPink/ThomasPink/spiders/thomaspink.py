"""
This module crawl pages and get data.
"""
import scrapy


class ThomasPinkSpider(scrapy.Spider):
    """This class crawl thomaspink pages"""
    name = 'thomaspink'
    next_page_flag = False

    def start_requests(self):
        """This method request for crawl orsay pages"""
        start_urls = 'https://www.thomaspink.com'
        yield scrapy.Request(url=start_urls, callback=self.parse)

    def parse(self, response):
        """This method crawl page urls."""
        for link in response.css('ul.level-1 li.f-nav-list__item--level-1'):
            level3_urls = link.css(
                'li.f-nav-list__item--level-3>a::attr(href)').extract()
            level2_link = link.css(
                'li.f-nav-list__item--level-2>a::attr(href)').extract()
            for link in level2_link:
                self.next_page_flag = False
                yield scrapy.Request(
                    url=link, callback=self.item_info_url)

            for link in level3_urls:
                self.next_page_flag = False
                yield scrapy.Request(
                    url=link, callback=self.item_info_url)

    def item_info_url(self, response):
        """This method crawl item detail url."""
        item_url = response.css(
            '.f-product-card__info>h2>a::attr(href)').extract()
        for url in item_url:
            item_url = response.urljoin(url)
            yield scrapy.Request(
                url=item_url, callback=self.item_detail)
        next_page_url = response.css(
            '.pagination>a::attr(href)').extract()
        if next_page_url:
            if not self.next_page_flag:
                next_url = next_page_url[0]
                self.next_page_flag = True
            else:
                if next_page_url[1]:
                    next_url = next_page_url[1]
            next_url = response.urljoin(next_url)
            yield scrapy.Request(
                url=next_url, callback=self.item_info_url)

    def item_detail(self, response):
        """This method crawl item detail information."""
        description = response.css('ul.f-tabs-content>li>div>p::text').extract()
        concatinate_description = ''.join(description)
        item_data = {
            'item_detail_url': response.url,
            'title':  response.css('.f-product-info__heading>h1::text').extract_first(),
            'price': response.css(
                '.f-product-info__meta>p>span::text').extract_first(),
            'item_id': response.css(
                '.f-product-info__meta>.f-product-info__id::attr(data-js-upk)').extract_first(),
            'description': concatinate_description,
            'delivery_details': response.css('ul.f-tabs-content>li>p>strong::text').extract(),
        }
        yield item_data
