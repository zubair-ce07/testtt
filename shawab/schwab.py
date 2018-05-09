from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider, Spider
from schwab.items import SchwabItem
from w3lib.url import add_or_replace_parameter, url_query_cleaner
import json


class Schwab(Spider):
    name = 'spider'
    stock_url = ['https://www.schwab.de/request/itemservice.php?fnc=getItemInfos']
    sku_counter = 0
    stock_counter = 0
    gender = {
        'Damen': 'Ladies',
        'Damenmode': 'Ladies',
        'Herren': 'Men',
        'Mädchen': 'Girls',
        'Jungen': 'Boys',
        'Baby Mädchen': 'Baby Girl',
        'Baby Jungen': 'Baby Boys',
        'Kinder': 'Children',
    }

    def parse_product(self, response):
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
        product['trail'] = self.product_trail(response)
        product['gender'] = self.product_gender(response)
        product['skus'] = self.product_skus(response)
        product['care'] = self.product_care(response)
        product['merch_info'] = "None"

        if not product['gender']:
            product['industry'] = "Homeware"

        self.sku_counter = 0
        self.stock_counter = 0
        addl_requests = self.addtional_colors_requests(response)
        return self.parse_additional_requests(addl_requests, product)

    def product_skus(self, response):
        sizes = self.product_size(response)
        previous_price = self.product_previous_price(response)
        total_skus = {}

        sku = {}
        sku["price"] = self.product_price(response)
        sku["currency"] = self.product_currency(response)
        sku["color"] = self.product_color(response)
        id = self.product_retailer_sku(response)

        if previous_price:
            sku['previous_prices'] = previous_price

        if not sizes:
            if previous_price:
                sku["sku_id"] = id + '|' + (sku['color'] or '') + '|' + sku['price']
                total_skus.update({self.sku_counter: sku})
                self.sku_counter = self.sku_counter + 1

        else:
            for size in sizes:
                sku = {}
                sku["size"] = size
                sku["price"] = self.product_price(response)
                sku["currency"] = self.product_currency(response)
                sku["color"] = self.product_color(response)
                id = self.product_retailer_sku(response)
                if sku['color'] and sku['price']:
                    sku["sku_id"] = id + '|' + sku['color'] + '|' + sku['size'] + '|' + sku['price']
                else:
                    sku["sku_id"] = id + '|' + '|' + sku['size'] + '|' + sku['price']
                total_skus.update({self.sku_counter: sku})
                self.sku_counter = self.sku_counter + 1
        return total_skus

    @staticmethod
    def additional_colors(response):
        colors = response.css('a.colorspots__item::attr(title)').extract()
        additional_urls = []

        for color in colors:
            full_url = add_or_replace_parameter(response.url, "color", color)
            additional_urls.append(full_url)

        return additional_urls

    def addtional_colors_requests(self, response):
        addl_colors_urls = self.additional_colors(response)

        additional_requests = []

        if addl_colors_urls:
            for request_url in addl_colors_urls:
                additional_requests += self.out_of_stock_request(response)
                additional_requests.append(Request(url=request_url, callback=self.parse_extra_images, dont_filter=True))
        else:
            url = self.product_url_origin(response)
            additional_requests += self.out_of_stock_request(response)
            additional_requests.append(Request(url=url, callback=self.parse_extra_stocks, dont_filter=True))
        return additional_requests

    def out_of_stock_request(self, response):
        item_number = response.css('script::text').re_first(r'articlesString(.+),(\d)')
        item_number = item_number[2:]
        items = {
            'items': item_number
        }
        return [FormRequest(url=self.stock_url[0], formdata=items, callback=self.parse_stock, dont_filter=True)]

    def parse_stock(self, response):
        product = response.meta['product']
        requests = response.meta['requests']
        raw_data = response.text

        stock_data = json.loads(raw_data)
        del stock_data['codes']
        del stock_data['express']
        sold_out = ['lieferbar innerhalb 3 Wochen', 'ausverkauft']

        for item in product['skus']:
            if product['skus'][item]:
                sku_id = product['skus'][item]['sku_id'].split('|')
                id = sku_id[0]
                size = sku_id[2]

                for stock in stock_data[id]:
                    stock = stock.strip()
                    if (stock == 0 or stock == size) and (stock_data[id][stock] in sold_out):
                        product['skus'][item]['out_of_stock'] = True

        return self.parse_additional_requests(requests, product)

    def parse_extra_images(self, response):
        product = response.meta['product']
        requests = response.meta['requests']
        product['skus'].update(self.product_skus(response))
        product['images_urls'] += self.product_images(response)
        return self.parse_additional_requests(requests, product)

    def parse_extra_stocks(self, response):
        product = response.meta['product']
        requests = response.meta['requests']
        return self.parse_additional_requests(requests, product)

    @staticmethod
    def parse_additional_requests(requests, product):
        if requests:
            request = requests[0]
            del requests[0]
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
        price = response.css('.js-wrong-price::text').extract_first()
        if price:
            return price.replace('.', '')
        return price

    @staticmethod
    def product_price(response):
        price = response.css('.js-detail-price::text').extract_first()
        return price.replace(',', '')

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
        for image in range(len(images)):
            images[image] = str("https:") + images[image]
        return images

    @staticmethod
    def product_retailer_sku(response):
        return response.css('.js-current-artnum::attr(value)').extract_first()

    @staticmethod
    def product_description(response):
        desc = response.css('div.l-outsp-bot-10 li::text').extract()
        return clean_product(desc)

    @staticmethod
    def product_url_origin(response):
        return response.css('link[rel="canonical"]::attr(href)').extract_first()

    def product_trail(self, response):
        trails = response.css('div#breadcrumb li>a::attr(href)').extract()

        category_counter = 0
        categories = self.product_category(response)
        trail_list = []

        for trail in trails:
            trail_list.append((categories[category_counter], trail))
            category_counter = category_counter + 1
        return trail_list

    def product_gender(self, response):
        categories = self.product_category(response)
        for category in categories:
            for gender in self.gender:
                if category == gender:
                    return gender
        else:
            return None

    @staticmethod
    def product_category(response):
        return response.css('div#breadcrumb a>span::text').extract()

    @staticmethod
    def product_color(response):
        return response.css('.js-current-color-name::attr(value)').re_first(r'(\w+)')

    @staticmethod
    def product_size(response):
        return response.css('.js-sizeSelector button::text').re(r'(\d+)')


class SchwabCralwer(CrawlSpider):
    name = 'schwab'
    allowed_domain = ['https://www.schwab.de/']
    main_url = 'https://www.schwab.de'
    start_urls = [
        'https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true&staticContent=true&cacheID=1525066940']

    spider_obj = Schwab()

    def parse_start_url(self, response):
        raw_urls = json.loads(response.text)

        for url in raw_urls:
            for inner_cat in url['sCat']:
                yield Request(url=inner_cat['url'], callback=self.parse_pagination)

    def parse_pagination(self, response):
        total_items = response.css('.pl__headline__count::text').re_first(r'(\d+)')
        items_per_page = 60

        if not total_items:
            return

        total_pages = (int(total_items) // items_per_page) + 1

        for page in range(1, total_pages):
            url = add_or_replace_parameter(response.url, 'pageNr', page)
            yield Request(url=url, callback=self.parse_next_page)

    def parse_next_page(self, response):
        product_requests = []
        products = response.css('div.product__top a::attr(href)').extract()

        for product in products:
            product_url = url_query_cleaner(self.main_url + product)
            product_requests.append(Request(url=product_url, callback=self.spider_obj.parse_product))
        return product_requests


def clean_product(raw_data):
    cleaned_list = []
    for item in raw_data:
        item = item.strip()
        if item:
            cleaned_list.append(item)
    return cleaned_list
