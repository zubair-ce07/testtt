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
        garment = SugarshapeItem()
        garment['retailer'] = 'sugarshape'
        garment['market'] = 'DE'
        garment['lang'] = 'de'
        garment['gender'] = 'women'
        garment['name'] = response.css('#productTitle span::text').extract_first()
        garment['brand'] = 'Sugar Shape'
        garment['description'] = response.css('#description p::text').extract()
        garment['category'] = response.css('#breadCrumb a:last-child::text').extract_first()
        garment['url'] = response.url
        garment['industry'] = None
        garment['currency'] = 'EUR'
        garment['image_urls'] = response.css('a[id ^="morePics"]::attr(href)').extract()
        garment['spider_name'] = self.name
        garment['price'] = self.product_price(response)
        garment['url_original'] = response.url
        care = self.product_care(response)
        garment['care'] = care
        garment['skus'] = {}
        related_urls = response.css('.SusColorBox > a::attr(href)').extract()

        return self.follow_related_pages(garment, related_urls)

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

    def product_description(self, response):
        return response.css('div#description > p::text').extract()

    def product_price(self, response):
        price = response.css('#productPrice div:nth-child(1)::text').extract_first()
        price = ''.join(price.strip().split(' ')[0].split(','))
        return price

    def product_sizes(self, response):
        return response.css('a.variantSelector::text').extract()
