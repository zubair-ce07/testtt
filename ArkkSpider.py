from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class ArkkSpider(CrawlSpider):
    name = "ArkkSpider"
    base_url = ['https://www.arkkcopenhagen.com']
    start_urls = ['https://www.arkkcopenhagen.com/collections/all-sneakers?page=1'
                  ]
    rules = (
        Rule(LinkExtractor(
            restrict_css='a.btn'),),
        Rule(LinkExtractor(
            restrict_css='a.grid-view-item__link.grid-view-item__image-container'), callback="parse_product"),)

    def parse_product(self, response):
        item = {
            'brand': response.xpath("//meta[@property='og:site_name']/@content").extract_first(),
            'name': response.css('.breadcrumb>span::text').extract()[2],
            'color': response.css('.product-single__color::text').extract_first(),
            'product_status': response.css('.product-card__banner--title::text').extract_first().strip(),
            'availability': {
                'gender': response.css('.product-single__sizing-title::text').extract_first(),
                'sizes': response.css('div.available>label::text').re("\d{2}"),
            },
            'sku': response.css('script').re('id"(.*?)",')[2:10],
            'img-url': response.urljoin(response.css('.feature-row__image::attr(src)').extract_first()),
            'material': response.css('.split-section__text::text').extract(),
            'price in euro': response.css('#ProductPrice-product-template::text').re_first("\d{3}"),
            'trails': {
                'back_url': response.urljoin(response.css('.breadcrumb>a::attr(href)').extract()[-1]),
                'product_url': response.request.url,
            },
        }
        yield item
