import json

from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import add_or_replace_parameter
from copy import deepcopy

from schwab.items import SchwabItem


class SchwabMixin:
    allowed_domain = ['https://www.schwab.de/']


class SchwabParserSpider(SchwabMixin, Spider):
    allowed_domain = SchwabMixin.allowed_domain

    name = 'schwab-parse'
    stock_url = 'https://www.schwab.de/request/itemservice.php?fnc=getItemInfos'
    size_url = 'https://www.schwab.de/index.php?'
    gender_map = {
        'damen': 'Women',
        'damenmode': 'Women',
        'damenbademode': 'Women',
        'herren': 'Men',
        'marken': 'Men',
        'mädchen': 'Girls',
        'ihn': 'Men',
        'jungen': 'Boys',
        'kinder': 'Unisex-kids',
        'festivalschuhe': 'Unisex-adults'
    }

    def product_package(self, response):
        product = SchwabItem()
        product['name'] = self.product_name(response)
        product['product_brand'] = self.product_brand(response)
        product['price'] = self.product_price(response)
        product['currency'] = self.product_currency(response)
        product['images_urls'] = self.product_images(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['description'] = self.product_description(response)
        product['url'] = self.product_url_origin(response)
        product['retailer'] = "schwab"
        product['category'] = self.product_category(response)
        product['trail'] = response.meta.get('trail', [])
        product['gender'] = self.product_gender(response)
        product['care'] = self.product_care(response)
        product['skus'] = {}
        product['merch_info'] = []

        if not product['gender']:
            product['industry'] = "Homeware"

        return self.extract_requests(self.color_requests(response), product)

    def parse_size(self, response):
        product = response.meta['product']
        requests = response.meta['requests']

        product['skus'].update(self.product_sku(response))
        return self.extract_requests(requests, product)

    def parse_stock(self, response):
        product = response.meta['product']
        requests = response.meta['requests']
        stocks = response.text

        stock_status = json.loads(stocks)
        sold_out = ['lieferbar innerhalb 3 Wochen', 'ausverkauft', 'lieferbar bis Mitte  Juli',
                    'lieferbar innerhalb 4 Wochen']

        for item in product['skus'].values():
            product_id = product['retailer_sku']
            size = item.get('size')

            if size:
                if stock_status[product_id].get(size) in sold_out:
                    item['out_of_stock'] = True
            elif stock_status[product_id][0] in sold_out:
                item['out_of_stock'] = True

        return self.extract_requests(requests, product)

    def parse_color(self, response):
        product = response.meta['product']
        requests = response.meta['requests']

        requests += self.size_request(response)

        requests += self.stock_request(response)

        product['skus'].update(self.product_sku(response))
        product['images_urls'] += self.product_images(response)

        return self.extract_requests(requests, product)

    def product_sku(self, response):
        previous_price = self.product_previous_price(response)
        sku = {}

        if previous_price:
            sku['previous_prices'] = previous_price

        sku["price"] = self.product_price(response)
        sku["currency"] = self.product_currency(response)
        sku["color"] = self.product_color(response)

        sku['size'] = response.meta.get('size', "One size")

        sku_id = '{color}|{size}'.format(color=(sku['color'] or ''), size=sku['size'])

        return {sku_id: sku}

    def color_requests(self, response):
        colors = response.css('a.colorspots__item::attr(title)').extract()
        requests = []

        for color in colors:
            url = add_or_replace_parameter(response.url, "color", color)
            requests += [Request(url=url, callback=self.parse_color, dont_filter=True)]

        # For handling those requests which doesn't has color_requests
        if not colors:
            requests += self.stock_request(response)
            requests += self.size_request(response)
        return requests

    def stock_request(self, response):
        item_number = response.css('script::text').re_first(r'articlesString(.+),(\d)')
        item_number = item_number[2:]
        items = {
            'items': item_number
        }
        return [FormRequest(url=self.stock_url, formdata=items, callback=self.parse_stock, dont_filter=True)]

    def size_request(self, response):
        params = {}
        requests = []

        varsel_ids = response.css('.js-variantSelector option::attr(value)').re(r'(\w+)') + \
                     response.css('.js-sizeSelector button::attr(data-varselid)').extract()
        size_ids = response.css(
            '.js-variantSelector option::attr(data-noa-size), .js-sizeSelector button::attr(data-noa-size)').extract()
        aid = response.css('input[name="aid"]::attr(value)').extract_first().split('-')
        anid = response.css('input[name="anid"]::attr(value)').extract_first().split('-')
        varselid_2 = response.css('input[name="varselid[2]"]::attr(value)').extract_first()
        varselid_1 = response.css('input[name="varselid[1]"]::attr(value)').extract_first()

        params["promo"] = response.css('input[name="promo"]::attr(value)').extract_first()
        params["artName"] = response.css('input[name="artName"]::attr(value)').extract_first()
        params["cl"] = response.css('div > input[name="cl"]::attr(value)').extract()[1]
        params["parentid"] = response.css('input[name="parentid"]::attr(value)').extract_first()

        if varselid_2:
            params["varselid[2]"] = varselid_2
        if varselid_1:
            params["varselid[1]"] = varselid_1

        if not (aid and anid):
            return

        for varsel, size in zip(varsel_ids, size_ids):
            if varsel:
                params["varselid[0]"] = varsel

            aid[2] = size
            anid[2] = size
            params['aid'] = '-'.join(aid)
            params['anid'] = '-'.join(anid)
            response.meta['size'] = size

            requests.append(
                FormRequest(url=self.size_url, formdata=params, callback=self.parse_size, meta=response.meta,
                            dont_filter=True))

        return requests

    @staticmethod
    def extract_requests(requests, product):
        if requests:
            request = requests.pop()
            request.meta['product'] = product
            request.meta['requests'] = requests
            yield request
        else:
            yield product

    @staticmethod
    def product_name(response):
        name = response.css('h1.details__title span::text').extract_first()
        return name.strip()

    @staticmethod
    def product_brand(response):
        return response.css('meta.at-dv-brand::attr(content)').extract_first()

    @staticmethod
    def product_previous_price(response):
        pre_price = response.css('.js-wrong-price::text').re(r'(\d+)')
        if pre_price:
            return int(''.join(pre_price))

    @staticmethod
    def product_price(response):
        price = response.css('.js-detail-price::text').re(r'(\d+)')
        return int(''.join(price))

    @staticmethod
    def product_currency(response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

    @staticmethod
    def product_care(response):
        cares = response.css('.details__desc__more__content div::text').extract()
        return clean_product(cares)

    @staticmethod
    def product_images(response):
        images = response.css('#thumbslider a::attr(href)').extract()
        return ["https:" + i for i in images]

    @staticmethod
    def product_retailer_sku(response):
        return response.css('.js-current-artnum::attr(value)').extract_first()

    @staticmethod
    def product_description(response):
        desc = response.css('div.l-outsp-bot-10 li::text').extract()
        return clean_product(desc)

    @staticmethod
    def product_sizes(response):
        sizes = response.css('.js-variantSelector option::text, .js-sizeSelector button::text').extract()
        return clean_product(sizes)

    @staticmethod
    def product_url_origin(response):
        return response.css('link[rel="canonical"]::attr(href)').extract_first()

    def product_gender(self, response):
        categories = self.product_category(response)

        for category in categories:
            category = category.lower()
            if category in self.gender_map:
                return self.gender_map[category]

    @staticmethod
    def product_category(response):
        return response.css('div#breadcrumb a>span::text').extract()

    @staticmethod
    def product_color(response):
        return response.css('.js-current-color-name::attr(value)').re_first(r'(\w+)')


class SchwabCralwer(SchwabMixin, CrawlSpider):
    name = 'schwab'
    items_per_page = 60
    start_url = 'https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true&staticContent=true&cacheID=1525066940'

    spider_parser = SchwabParserSpider()

    allowed_domain = SchwabMixin.allowed_domain

    rules = (
        Rule(LinkExtractor(restrict_css='div.product__top'), callback=spider_parser.product_package),
    )

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse_listing)

    def parse_listing(self, response):
        raw_urls = json.loads(response.text)
        for url in raw_urls:
            for inner_cat in url['sCat']:
                yield Request(url=inner_cat['url'], callback=self.parse_pagination)

    def parse_pagination(self, response):
        common_meta = {}
        common_meta['trail'] = [response.url]

        total_items = response.css('.pl__headline__count::text').re_first(r'(\d+)')
        if not total_items:
            return

        total_pages = (int(total_items) // self.items_per_page) + 1

        for page in range(1, total_pages):
            url = add_or_replace_parameter(response.url, 'pageNr', page)
            meta = deepcopy(common_meta)
            yield Request(url=url, callback=self.parse, meta=meta)

    def parse(self, response):
        response.meta['trail'] = response.meta.get('trail', [])
        response.meta['trail'] += [response.url]

        for request in super().parse(response):
            request.meta['trail'] = response.meta['trail']
            yield request


def clean_product(raw_data):
    cleaned_list = []
    for item in raw_data:
        item = item.strip()
        if item:
            cleaned_list.append(item)
    return cleaned_list
