from scrapy import Request
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ThomasPink(CrawlSpider):
    """Its a Scrapy Crawler class which traverses and scraps data from ThomasPink Website"""

    # Crawler Name
    name = "thomaspink"

    # Thomaspink Website Link
    start_urls = ['https://www.thomaspink.com/']

    # Rules used while extracting links from Thomaspink Website
    rules = (
        Rule(
            LinkExtractor(restrict_css=["a.f-nav-list__item-link--level-3"]), callback='parse_page'
        ),
    )

    def parse_page(self, response):
        """Takes response of website as argument, extracts item urls and do pagination"""

        # Extracting all item urls from web response
        items_urls = response.css('ol.f-product-list li.f-product-list__item::attr(data-product-url)').extract()

        # Iterating over items
        for item_url in items_urls:
            yield self.parse_item_url(item_url)

        # Check pagination of the web-page
        yield self.do_pagination(response)

    def do_pagination(self, response):
        """Takes response of web-page as argument, checks if pagination exists and return next page's link"""

        # Extracting next page link
        url_next = response.css('a.pagination__arrow[rel=next]::attr(href)').extract_first()

        # If next page exists return it otherwise return None
        if url_next:
            return response.follow(url_next, self.parse_page)

    def parse_item_url(self, item_url):
        """Takes item-url as argument and concatenate it to form an appropriate link, to get data from it"""
        url = 'https://www.thomaspink.com' + item_url
        if item_url:
            return Request(url=url, callback=self.get_item_info)

    def get_item_info(self, response):
        """Takes response of web-page as argument and extracts necessary information in the form of dict"""

        # Extracting information
        item_id = response.css('p.f-product-info__id::attr(data-js-upk)').extract_first().encode('utf-8')
        images = response.css('img.cloudzoom::attr(src)').extract()
        colors = response.css('ul.f-product-colours__list img::attr(alt)').extract()
        sizes = response.css(
            'ul.f-product-buy-form__size-list li:not(.f-selection-block--no-stock) label::text').extract()
        title = response.css('h1[itemprop="name"]::text').extract_first()
        price = response.css('span.f-block-price__item::text').extract_first()
        description = response.css('li[data-js-method="description"] p::text').extract_first()
        qualities = response.css('li[data-js-method="description"] ul>li::text').extract()

        # returning dictionary
        return {
            str(item_id): {
                'images': images, 'sizes': sizes,
                'colors': colors, 'title': title,
                'description': description, 'price': price,
                'qualities': qualities
            }
        }
