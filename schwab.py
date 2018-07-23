import json
import re

from scrapy import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import Request
from urllib.parse import urlencode

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'schwab'
    market = 'DE'
    allowed_domains = ['schwab.de']
    start_urls = ['https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true&staticContent=true']
    base_url = 'https://www.schwab.de/index.php?'
    info_api_url = 'https://www.schwab.de/request/itemservice.php?fnc=getItemInfos'


class SchwabParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    description_css = 'div[itemprop=description] ::text'
    care_css = '.details__variation__hightlights ::text'
    price_css = '.js-wrong-price pricing__norm--wrong__price ::text, ' \
                '.js-detail-price ::text, ' \
                'meta[itemprop=priceCurrency] ::attr(content)'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.gender(garment['category'])
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.colours_size_request(response)}
        garment['meta']['requests_queue'].append(self.product_information_requests(response))
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

    def gender(self, category):
        return self.gender_lookup(''.join(map(str, category))) or 'unisex-adults'

    def image_urls(self, response):
        image_urls = clean(response.css('a[id=magic] ::attr(href)'))
        return [response.urljoin(url) for url in image_urls]

    def stock_check(self, response, size):
        size = 0 if size == self.one_size else size
        garment = response.meta['garment']
        product_information = garment['meta']['information']
        article_id = clean(response.css('input[name=artNr] ::attr(value)'))[0]
        if 'ausverkauft' in product_information[article_id][size]:
            return True
        return False

    def skus(self, response):
        colour_css = '.js-current-color-name ::attr(value)'
        size_css = '.js-current-size-name ::attr(value)'
        length_css = '.js-current-variant-name ::attr(value)'
        sku = self.product_pricing_common(response)
        size = response.css(size_css).extract_first(default='')
        size = self.one_size if not size else size
        sku['colour'] = colour = response.css(colour_css).extract_first(default='')
        sku['size'] = size
        sku['length'] = response.css(length_css).extract_first(default='')
        sku['out_of_stock'] = self.stock_check(response, size)
        sku_id = f'{colour}_{size}' if colour else f'{size}'
        return {sku_id: sku}

    def colours_size_request(self, response):
        requests = []
        anids = self.product_articles(response)
        for anid in anids:
            form_data = {
                'cl': clean(response.css('#detailsMain input[name="cl"]::attr(value)'))[0],
                'anid': anid,
                'ajaxdetails': 'ajaxdetailsPage',
                'parentid': self.product_id(response)
            }
            requests += [FormRequest(url=self.base_url,
                                     formdata=form_data,
                                     callback=self.parse_size_colours,
                                     )]
        return requests

    def product_information_requests(self, response):
        form_data = {
            'items': self.articles(response)
        }
        return FormRequest(url=self.info_api_url,
                           formdata=form_data,
                           callback=self.parse_info,
                           )

    def image_requests(self, response):
        varselid = clean(response.css('.js-varselid-COLOR ::attr(value)'))
        if not varselid:
            return []
        query_string_data = {
            'cl': 'oxwarticledetails',
            'anid': clean(response.css('.js-current-articleid ::attr(value)'))[0],
            'ajaxdetails': 'adsColorChange',
            'varselid[2]': varselid,
        }
        return [Request(url=f'{self.base_url}{urlencode(query_string_data)}',
                        method="GET",
                        callback=self.parse_images,
                        )]

    def parse_info(self, response):
        garment = response.meta['garment']
        garment['meta']['information'] = json.loads(response.body)
        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def parse_size_colours(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['meta']['requests_queue'] += self.image_requests(response)
        return self.next_request_or_garment(garment)

    def articles(self, response):
        articles = clean(response.xpath("//script[contains(text(),'articlesString')]/text()"))[0]
        articles_information = re.findall('\d+\|\d+\|[A-Z0-9|;,]+', articles)
        return articles_information[0]

    def product_articles(self, response):
        articles = self.articles(response).split(';')
        product_id = self.product_id(response)
        anids = []
        for article in articles:
            identity, article_id, colour, size = article.split('|')
            if size == '0':
                anids.append(f"{product_id}-{article_id}-{colour}")
            else:
                anids.append(f"{product_id}-{article_id}-{size}-{colour}")
        return anids


class SchwabSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = SchwabParseSpider()
    listing_css = ['.js-next']
    product_css = '.js-pl-product'
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_categories)

    def parse_categories(self, response):
        response_data = json.loads(response.text)
        for categories in response_data:
            for sub_category in categories['sCat']:
                for category in sub_category.get('sCat', {}):
                    yield Request(url=category['url'], callback=self.parse)

