"""
This module crawl pages and get data.
"""
import re
import scrapy


class SheegoSpider(scrapy.Spider):
    """This class crawl Sheego pages"""
    name = 'sheego'

    def start_requests(self):
        """This method request for crawl orsay pages"""
        start_urls = 'https://www.sheego.de/'
        yield scrapy.Request(url=start_urls, callback=self.parse)

    def parse(self, response):
        """This method crawl page urls."""
        for link in response.css('.cj-mainnav__contents'):
            level1_link = link.css(
                '.cj-mainnav__contents>div>a::attr(href)').extract()
            for link in level1_link:
                yield scrapy.Request(
                    url=link, callback=self.item_info_url)

    def item_info_url(self, response):
        """This method crawl item detail url."""
        item_url = response.css(
            'div.product__wrapper--bottom>a::attr(href)').extract()
        for url in item_url:
            if url != '#':
                item_url = response.urljoin(url)
                yield scrapy.Request(
                    url=item_url, callback=self.item_detail)
        next_page = response.css(
            'div.pl__head__paging--right>div>span.paging__btn--next>a::attr(href)').extract_first()
        if next_page:
            # checking if their is next page
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(
                url=next_page_url, callback=self.item_info_url)

    def item_detail(self, response):
        """This method crawl item detail information."""
        size = []
        pattern = "^[A-Z\d/\s]+$"
        title = response.css('span.p-details__name::text').extract_first()
        item_size = response.css('div.c-sizespots>div::text').extract()
        for data in item_size:
            modified_data = re.match(pattern, data, flags=re.MULTILINE)
            if modified_data:
                size.append(modified_data.group().strip())
            else:
                size.append(data)
        item_data = {
            'item_detail_url': response.url,
            'category': response.css(
                'div.cj-p-details__variants>div>h1>span::text').extract_first().strip(),
            'product_title': title.strip(),
            'price': response.css(
                'div.cj-p-details__variants>div>section>span::text').extract_first().strip(),
            'sizes': size,
            'description': response.css('div.l-mb-5>.l-list--nospace>li::text').extract(),
        }
        yield item_data
