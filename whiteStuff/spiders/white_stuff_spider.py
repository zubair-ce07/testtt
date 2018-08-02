import re
import json
import urllib.parse
import datetime

from scrapy import Spider, Request, Selector

from whiteStuff import items


class WhiteStuffSpider(Spider):
    todays_date = datetime.date.today()
    DOWNLOAD_DELAY = 1
    name = 'white_stuff'
    start_urls = ['https://www.whitestuff.com/global']
    skus_request_url = "https://www.whitestuff.com/global/action/GetProductData-FormatProduct?"
    base_url = 'https://www.whitestuff.com/global'
    headers = {
        'Referer': 'https://www.whitestuff.com/global/womens/new-in/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }

    params = {
        'version': '18.2.4',
        'siteId': 'c7439161-d4f1-4370-939b-ef33f4c876cc',
        'UID': '20236a83-6a7c-a88e-cad2-542daa8a9c49',
        'SID': '42a0e829-b36c-95b3-0f44-16a64cc60069',
        'referrer': 'https://www.whitestuff.com/global/',
        'sitereferrer': '',
        'pageurl': '',
        'zone0': 'banner',
        'zone1': 'category',
        'zone2': 'advert1',
        'zone3': 'advert2',
        'zone4': 'advert3',
        'facetmode': 'data',
        'mergehash': 'true',
        'culture': 'en-IE',
        'currency': 'EUR',
        'language': 'en-GB',
        'config_categorytree': '',
        'config_category': '',
        'config_region': 'WhiteStuff_ROW',
        'config_brand': 'null',
        'config_colour': 'null',
        'config_producttype': 'null',
        'config_fsm_sid': '42a0e829-b36c-95b3-0f44-16a64cc60069',
        'config_fsm_returnuser': '1',
        'config_fsm_currentvisit': f'{todays_date.day:02}/{todays_date.month:02}/{todays_date.year}',
        'config_fsm_visitcount': '8',
        'config_fsm_lastvisit': '31/07/2018',
    }

    def parse(self, response):
        links = set(response.css('.navbar__item a::attr(href)').extract())
        filters = ['kids', 'mens', 'gift']
        for link in links:
            for filter_ in filters:
                if filter_ in link:
                    yield Request(url=link, callback=self.first_visit)

    def first_visit(self, response):
        try:
            categories = [response.css('script::text').extract()[6].split('"')[-2],
                         response.css('script::text').extract()[6].split('"')[-4]]
            local_params = self.params.copy()
            local_params['config_categorytree'] = categories[1]
            local_params['config_category'] = categories[0]
            local_params['pageurl'] = response.url
            r2 = Request(url=f'https://fsm.attraqt.com/zones-js.aspx?{urllib.parse.urlencode(local_params)}',
                         headers=self.headers, method="GET", callback=self.parse_full_response)
            r2.meta['url'] = response.url
            r2.meta['config_categorytree'] = categories[1]
            r2.meta['config_category'] = categories[0]
            yield r2
        except:
            pass

    def parse_full_response(self, response):
        try:
            response_url = response.meta.get('url')
            category_tree = response.meta.get('config_categorytree')
            category = response.meta.get('config_category')
            response = json.loads(response.text.split('LM')[-2].strip('.buildZone(').split(');')[0])['html']
            selector = Selector(text=response)
            product_urls = [urllib.parse.urljoin(self.base_url, a) for a in
                            selector.css('.product-tile__title a::attr(href)').extract()]
            for url in product_urls:
                yield Request(url=url, callback=self.parse_item)
            total_pages = int(selector.css('#TotalPages::attr(value)').extract_first() or '1')
            if response_url and total_pages > 1:
                local_parameters = self.params.copy()
                local_parameters['config_categorytree'] = category_tree
                local_parameters['config_category'] = category
                for page_no in range(2, total_pages):
                    next_url = response_url + f'/#esp_pg={page_no}'
                    local_parameters['pageurl'] = next_url
                    yield Request(
                        url=f'https://fsm.attraqt.com/zones-js.aspx?{urllib.parse.urlencode(local_parameters)}',
                        headers=self.headers, method="GET", callback=self.parse_full_response)
        except:
            pass

    def parse_item(self, response):
        item = items.WhiteStuffItem()
        item['name'] = self.get_title(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['gender'] = self.get_gender(response)
        item['brand'] = 'White Stuff'
        item['categories'] = self.get_categories(response)
        item['url'] = self.get_url(response)
        item['description'], item['care'] = self.get_description_and_care(response)
        item['currency'] = self.get_currency(response)
        get_skus_url = self.make_json_request_url(response)
        request = Request(url=get_skus_url, method="GET", callback=self.get_skus)
        request.meta['item'] = item
        yield request
        return item

    def get_skus(self, response):
        item = response.meta['item']
        json_response = json.loads(re.sub('\\\\\'', "",
                                          re.sub('//this.*\n', "", response.text.split('=')[1].split(';')[0])))
        skus = json_response['productVariations']
        for sku_id in skus.keys():
            sku = skus.get(sku_id)
            imgs = []
            for image in sku["images"]:
                if image["size"] == "ORI":
                    imgs.append(image['src'])
            skus[sku_id]["images"] = imgs
        item['skus'] = self.make_skus(skus)
        return item

    @staticmethod
    def format_price(price):
        price = price.translate(str.maketrans({u"\u20ac": ''}))
        return int(float(price) * 100)

    def make_skus(self, skus):
        my_skus = []
        for sku in skus.values():
            my_sku = {}
            my_sku['sku_id'] = sku['productUUID']
            my_sku['in_stock'] = sku['inStock']
            my_sku['colour'] = sku['colour']
            my_sku['size'] = sku['size']
            my_sku['image_urls'] = sku['images']
            my_sku['price'] = self.format_price(sku['salePrice'])
            if self.format_price(sku['salePrice']) < self.format_price(sku['listPrice']):
                my_sku['old-price'] = self.format_price(sku['listPrice'])
            my_skus.append(my_sku)
        return my_skus

    def make_json_request_url(self, response):
        sku_id = response.css('.js-variation-attribute::attr(data-variation-master-sku)').extract_first()
        parameters = {"Format": "JSON", "ReturnVariable": "true", "ProductID": sku_id}
        return f'{self.skus_request_url}{urllib.parse.urlencode(parameters.copy())}'

    @staticmethod
    def get_title(response):
        return response.css('.product-info__heading::text').extract()

    @staticmethod
    def get_retailer_sku(response):
        return response.css('[itemprop="sku"]::text').extract()

    @staticmethod
    def get_categories(response):
        return response.css('.breadcrumb-list__item-link::text').extract()[1:]

    @staticmethod
    def get_gender(response):
        genders = {"womens": "female", "mens": "male", "boys": "boy", "girls": "girl"}
        for gender in genders.keys():
            if gender in response.url:
                return genders.get(gender)

    @staticmethod
    def get_description_and_care(response):
        types = response.css('.ish-productAttributes .ish-ca-type::text').extract()
        values = response.css('.ish-productAttributes .ish-ca-value::text').extract()
        care = []
        description_care = list(zip(types, values))
        description = []
        for a in description_care:
            a = f'{a[0]} {a[1]}'
            if 'Care' in a:
                care.append(a)
            else:
                description.append(a)
        return description, care

    @staticmethod
    def get_url(response):
        return response.url

    @staticmethod
    def get_currency(response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()
