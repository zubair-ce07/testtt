import w3lib.url

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'finishline'
    allowed_domains = ['finishline.com']
    market = 'US'
    start_urls = [
        'http://www.finishline.com',
    ]


class FinishLineParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    image_api_url = 'http://www.finishline.com/store/browse/gadgets/alternateimage.jsp'
    price_css = '.fullPrice::text, .maskedFullPrice::text, .nowPrice::text, .wasPrice::text'
    gender_map = [
        ('women', 'women'),
        ('womens', 'women'),
        ('men', 'men'),
        ('mens', 'men'),
        ('kid', 'unisex-kids'),
        ('kids', 'unisex-kids'),
    ]

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return
        garment['gender'] = self.product_gender(response)
        self.boilerplate_normal(garment, response)
        garment['skus'] = self.skus(response)

        garment['image_urls'] = self.image_urls(response)
        garment['merch_info'] = self.merch_info(response)
        garment['meta'] = {'requests_queue': self.image_requests(response)}

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        sample_sku_id = clean(response.css('a[data-productid]::attr(data-productid)'))[0]
        if sample_sku_id:
            return sample_sku_id.split('-')[0]

    def product_name(self, response):
        return clean(response.css('h1#title::text'))[0]

    def product_brand(self, response):
        return clean(
            response.css('.maxUnitsPerOrderItem + script + script::text').re_first(r'FL.setup.brand = "(.*?)";'))

    def merch_info(self, response):
        raw_merch_info = clean(response.css('.specialMessaging::text'))
        if raw_merch_info:
            merch_info = list()
            for sentence in raw_merch_info:
                merch_info += sentence.split(',')
            raw_merch_info = list(set(merch_info))
            del merch_info[:]
            for sentence in raw_merch_info:
                if 'shipping' not in sentence.lower():
                    merch_info.append(sentence)
            return merch_info

    def raw_description(self, response):
        raw_description = clean(response.css('div#productDescription ::text'))[1:]
        final_raw_description = list()
        for sentence in raw_description:
            final_raw_description += clean(sentence.split('.'))
        return final_raw_description

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def product_category(self, response):
        return clean(response.css('ul.breadcrumbs li [itemprop="name"]::text'))[1:]

    def product_gender(self, response):
        gender_info = clean(response.css('[data-gender]::attr(data-gender)'))
        if gender_info:
            gender_info = gender_info[0].lower()
        else:
            gender_keys = [k for k, v in self.gender_map]
            for breadcrumb in clean(response.css('ul.breadcrumbs li [itemprop="name"]::text')):
                if breadcrumb.lower() in gender_keys:
                    gender_info = breadcrumb.lower()
        for gender_str, gender in self.GENDER_MAP:
            if gender_str in gender_info:
                return gender

    def product_colors(self, response):
        result = list()
        for item in response.css('#productStyleColor div.stylecolor'):
            result.append({
                'id': clean(item.css('.styleColorIds::text')[0]),
                'color': clean(item.css('.description::text')[0])
            })
        for item in result:
            item['colorid'] = item['id'].split()[-1]
        return result

    def skus(self, response):
        colors = self.product_colors(response)
        result = dict()
        for color in colors:
            price_info = response.css('#prices_{}'.format(color['id'].replace(' ', '-')))
            prices = self.product_pricing_common_new(price_info)
            color['price'] = prices['price']
            color['currency'] = prices['currency']
            if 'previous_prices' in prices:
                color['previous_prices'] = prices['previous_prices']
        for color in colors:
            complete_id = color['id']
            color_id = color['colorid']
            del color['colorid']
            del color['id']
            for size in response.css('#sizes_{} div.size'.format(complete_id.replace(' ', '-'))):
                if size.css('.NONE'):
                    size_value = self.one_size
                else:
                    size_value = clean(size.css('::text'))[0]
                if size.css('.unavailable'):
                    out_of_stock = True
                else:
                    out_of_stock = False
                result['{0}_{1}'.format(color_id, size_value)] = {
                    'out_of_stock': out_of_stock,
                    'size': size_value
                }
                result['{0}_{1}'.format(color_id, size_value)].update(color)
        return result

    def image_urls(self, response):
        image_urls = list()
        for image_url in clean(response.css('div#alt::attr(data-large)')):
            image_urls.append(image_url.replace(' ', ''))
        return image_urls

    def colorids_and_styleids(self, response):
        results = list()
        for color in response.css('a[data-productid]')[1:]:
            results.append({
                'colorID': clean(color.css('::attr(data-productid)'))[0],
                'styleID': clean(color.css('::attr(data-styleid)'))[0]
            })
        return results

    def product_url_name(self, response):
        return clean(response.css('.bVProductName::attr(value)'))[0]

    def product_item_id(self, response):
        return clean(response.css('[data-productitemId]::attr(data-productitemid)'))[0]

    def product_is_shoe(self, response):
        return clean(response.css('[data-productisshoe]::attr(data-productisshoe)'))[0]

    def product_is_accessory(self, response):
        return clean(response.css('[data-productisaccessory]::attr(data-productisaccessory)'))[0]

    def image_requests(self, response):
        request_query_strings = self.colorids_and_styleids(response)
        requests = list()
        request_url = self.image_api_url
        request_url = w3lib.url.add_or_replace_parameter(request_url, 'productIsAccessory',
                                                         self.product_is_accessory(response))
        request_url = w3lib.url.add_or_replace_parameter(request_url, 'productIsShoe', self.product_is_shoe(response))
        request_url = w3lib.url.add_or_replace_parameter(request_url, 'productItemId', self.product_item_id(response))
        request_url = w3lib.url.add_or_replace_parameter(request_url, 'productName', self.product_url_name(response))
        for request_qs in request_query_strings:
            temp_request_url = w3lib.url.add_or_replace_parameter(request_url, 'colorID', request_qs['colorID'])
            temp_request_url = w3lib.url.add_or_replace_parameter(temp_request_url, 'styleID', request_qs['styleID'])
            request = Request(temp_request_url, callback=self.parse_image_request)
            request.headers.update({
                'X-Requested-With': 'XMLHttpRequest'
            })
            requests.append(request)
        return requests

    def parse_image_request(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)


class FinishLineCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    listing_css = (
        '.Men-menu-dropdown div a',
        '.Women-menu-dropdown div a',
        '.Kids-menu-dropdown div a'
    )
    parse_spider = FinishLineParseSpider()
    pagination_css = 'div[class="paginationDiv"] a'
    products_css = '.product-container a:first_child'
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), follow=True),
        Rule(LinkExtractor(restrict_css=pagination_css), follow=True),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
