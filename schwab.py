from scrapy import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from .base import BaseParseSpider, BaseCrawlSpider, clean
from scrapy.http import Request
from urllib.parse import urljoin
import json
import re


class Mixin:
    retailer = 'schwab'
    market = 'DE'
    allowed_domains = ['schwab.de']
    start_urls = [
        'https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true&staticContent=true&cacheID=1531715824']
    url_api = 'https://www.schwab.de/index.php?'


class SchwabParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    description_css = 'div[itemprop=description] ::text'
    care_css = '.details__variation__hightlights ::text'
    price_css = '.js-wrong-price pricing__norm--wrong__price ::text, ' \
                '.js-detail-price ::text, ' \
                'meta[itemprop=priceCurrency] ::attr(content)'
    gender_map = [
        ('Damen', 'women'),
        ('Herren', 'men'),
        ('Madchen', 'girls'),
        ('Jungen', 'boys'),

    ]

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.colors_size_request(response)}
        return self.next_request_or_garment(garment)

    @staticmethod
    def product_id(response):
        return clean(response.css('.js-current-parentid ::attr(value)'))[0]

    @staticmethod
    def product_name(response):
        return clean(response.css('span[itemprop=name] ::text'))[0]

    @staticmethod
    def product_brand(response):
        return clean(response.css('meta[itemprop=brand] ::attr(content)'))

    @staticmethod
    def product_category(response):
        return clean(response.css('.breadcrumb [itemprop="name"]::text'))

    def gender(self, response):
        category = self.product_category(response)
        for gender, l_gender in self.gender_map:
            if gender in category:
                return l_gender
        if 'Kinder' in category:
            return 'unisex-kids'
        return 'unisex-adults'

    def image_urls(self, response):
        image_urls = clean(response.xpath('.//a[@id="magic"]/@href'))
        return [urljoin(self.url_api, url) for url in image_urls]

    def skus(self, response):
        color_css = '.js-current-color-name ::attr(value)'
        size_css = '.js-current-size-name ::attr(value)'
        color = response.css(color_css).extract_first(default='')
        size = response.css(size_css).extract_first(default='')
        sku = self.product_pricing_common(response)
        sku_id = "{}_{}".format(color, size)
        sku['color'] = color
        sku['size'] = size
        return {sku_id: sku}

    def colors_size_request(self, response):
        requests = []
        anids = self.product_articles(response)
        for anid in anids:
            form_data = {
                'cl': clean(response.css('#detailsMain input[name="cl"]::attr(value)'))[0],
                'anid': anid,
                'ajaxdetails': 'ajaxdetailsPage',
                'parentid': self.product_id(response)
            }
            requests += [FormRequest(url=self.url_api,
                                     formdata=form_data,
                                     callback=self.parse_size_colors,
                                     )]
        return requests

    def image_requests(self, response):
        varselid = clean(response.css('.js-varselid-COLOR ::attr(value)'))
        if not varselid:
            return []
        form_data = {
            'cl': 'oxwarticledetails',
            'anid': clean(response.css('.js-current-articleid ::attr(value)'))[0],
            'ajaxdetails': 'adsColorChange',
            'varselid[2]': varselid,
        }
        return [FormRequest(url=self.url_api,
                            formdata=form_data,
                            method="GET",
                            callback=self.parse_images,
                            )]

    def parse_images(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def parse_size_colors(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['meta']['requests_queue'] += self.image_requests(response)
        return self.next_request_or_garment(garment)

    def articles(self, response):
        articles_string = clean(response.xpath("//script[contains(text(),'articlesString')]/text()"))[0]
        data = re.findall('\d+\|\d+\|[A-Z0-9|;,]+', articles_string)
        return data[0].split(';')

    def product_articles(self, response):
        articles = self.articles(response)
        product_id = self.product_id(response)
        anids = []
        for article in articles:
            identity, articleid, color, size = article.split('|')
            if size == '0':
                anids.append("{}-{}-{}".format(product_id, articleid, color))
            else:
                anids.append("{}-{}-{}-{}".format(product_id, articleid, size, color))
        return anids


class SchwabSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = SchwabParseSpider()
    listing_css = [
        '.js-next'
    ]
    productCard_css = '.js-pl-product'

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_categories)

    def parse_categories(self, response):
        response_data = json.loads(response.body)
        for categories in response_data:
            for sub_category in categories['sCat']:
                if 'sCat' in sub_category:
                    for category in sub_category['sCat']:
                        yield Request(url=category['url'], callback=self.parse)

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css)
             ),
        Rule(
            LinkExtractor(restrict_css=productCard_css), callback='parse_item'
        )
    )
