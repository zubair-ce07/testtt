import re
import scrapy
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from sugarshape.items import SugarshapeItem


class SugarShapeSpider(CrawlSpider):
    name = "sugarshape"
    allowed_domains = ["sugarshape.de"]
    start_urls = [
        "http://sugarshape.de/shop",
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=['#SusCategoryBox', 'div.pager'])),
        Rule(LinkExtractor(restrict_css=['#SusGridProductTitle', '#SusCategoryGridImage']), callback='parse_items')
    )

    def parse_items(self, response):
        self.log(response.url)
        item = SugarshapeItem()
        item['retailer'] = 'sugarshape'
        item['market'] = 'DE'
        item['lang'] = 'de'
        item['gender'] = 'women'
        item['name'] = response.css('#productTitle span::text').extract_first()
        item['brand'] = 'Sugar Shape'
        item['description'] = '\n'.join(response.css('#description p::text').extract())
        item['category'] = response.css('#breadCrumb a:last-child::text').extract_first()
        item['url'] = response.url
        item['industry'] = None
        item['currency'] = 'EUR'
        item['image_urls'] = response.css('a[id ^="morePics"]::attr(href)').extract()
        item['spider_name'] = self.name
        item['price'] = self.product_price(response)
        item['url_original'] = response.url
        care = self.product_care(response)
        item['care'] = care
        item['skus'] = {}
        related_urls = response.css('.SusColorBox > a::attr(href)').extract()

        return self.follow_related_pages(item, related_urls)

    def follow_related_pages(self, item, related_urls):
        if related_urls:
            url = related_urls.pop()
            return scrapy.Request(url,
                                  callback=self.parse_related_page,
                                  meta={'item': item,
                                        'related_urls': related_urls,
                                        }
                                  )
        return item

    def parse_related_page(self, response):
        item = response.meta['item']
        related_urls = response.meta['related_urls']

        price = self.product_price(response)
        currency = 'EUR'
        color = self.product_color(response)
        sizes = self.product_sizes(response)
        self.log(sizes)

        skus = map(lambda size: {
            'price': price,
            'currency': currency,
            'color': color,
            'size': size
        }, sizes)

        for sku in skus:
            item['skus'].update({
                color + '_' + sku['size']: sku
            })
        return self.follow_related_pages(item, related_urls)

    def product_color(self, response):
        description_lines = self.product_description(response)
        color_pattern = '^farbe: (.*)'
        matches = filter(lambda line: re.match(color_pattern, line.strip().lower()), description_lines)
        if matches:
            color = re.match(color_pattern, matches[0].strip().lower()).group(1).strip()
            return color

        return None

    def product_care(self, response):
        description_lines = self.product_description(response)
        care_pattern = '^Material: (.*)'
        matches = filter(lambda line: re.match(care_pattern, line.strip()), description_lines)
        if matches:
            care = re.match(care_pattern, matches[0].strip()).group(1)
            return care

        return None

    @staticmethod
    def product_description(response):
        return response.css('div#description > p::text').extract()

    @staticmethod
    def product_price(response):
        price = response.css('#productPrice div:nth-child(1)::text').extract_first()
        price = ''.join(price.strip().split(' ')[0].split(','))
        return price

    @staticmethod
    def product_sizes(response):
        return response.css('a.variantSelector::text').extract()
