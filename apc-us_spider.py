from scrapy.spiders import Spider


class ApcProductsSpider(Spider):
    name = 'apc-us'
    start_urls = [
        'https://www.apc-us.com',
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,
    }
    allowed_domains = [
        'https://www.apc-us.com'
    ]

    def parse(self, response):
        for headers_url in response.css('nav li.nav-primary-item'):
            sub_url = headers_url.css('div ul.nav-sublevel a::attr(href)')
            if sub_url.get():
                yield {
                    'url': sub_url.getall(),
                }