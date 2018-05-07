from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from schwab.items import SchwabItem
from w3lib.url import add_or_replace_parameter, url_query_cleaner
import json


class Schwab(CrawlSpider):
    name = 'schwab'
    allowed_domain = ['https://www.schwab.de/']
    sku_counter = 0
    stock_counter = 0
    start_urls = ['https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true&staticContent=true&cacheID=1525066940']
    gender_dict = {
        'Damen': 'Ladies',
        'Damenmode': 'Ladies',
        'Herren': 'Men',
        'Mädchen': 'Girls',
        'Jungen': 'Boys',
        'Baby Mädchen': 'Baby Girl',
        'Baby Jungen': 'Baby Boys',
        'Kinder': 'Children',
    }

    def parse_start_url(self, response):
        raw_urls = json.loads(response.text)
        pages_urls = []
        pages_requests = []
        count = 0

        for url in raw_urls:
            if count == 0:
                pages_urls.append(url['url'])
                for inner_cat in url['sCat']:
                    pages_urls.append(inner_cat['url'])
            count = count + 1

        for page in pages_urls:
            pages_requests.append(Request(url=page, callback=self.parse_pagination))
        return pages_requests

    def parse_pagination(self, response):
        total_items = response.css('.pl__headline__count::text').re_first(r'(\d+)')
        items_per_page = 60

        if not total_items:
            return

        total_pages = (int(total_items) // items_per_page) + 1

        # 1 added for upper bound
        for page in range(total_pages + 1):
            if page == 0:
                yield Request(response.url, callback=self.parse_individual_request)
            else:
                url = add_or_replace_parameter(response.url, 'pageNr', page)
                yield Request(url=url, callback=self.parse_individual_request)

    def parse_individual_request(self, response):
        main_url = 'https://www.schwab.de'
        product_requests = []
        products = response.css('div.product__top a::attr(href)').extract()
        for product in products:
            join_url = url_query_cleaner(main_url + product)
            product_requests.append(Request(url=join_url, callback=self.parse_product))
        return product_requests

    def out_of_stock_request(self, response):
        url = ['https://www.schwab.de/request/itemservice.php?fnc=getItemInfos']
        post_request_data = response.css('script::text').re_first(r'articlesString(.+),(\d)')
        post_request_data = post_request_data[2:]
        items = {
            'items': post_request_data
        }
        return [FormRequest(url=url[0], formdata=items, callback=self.parse_stock_request, dont_filter=True)]

    def parse_stock_request(self, response):
        product = response.meta['product']
        requests = response.meta['requests']
        raw_data = response.text

        stock_data = json.loads(raw_data)
        del stock_data['codes']
        del stock_data['express']

        if product['skus'][self.stock_counter]['sku_id']:
            sku_id = product['skus'][self.stock_counter]['sku_id']
            sku_id = sku_id.split('|')[0]

            for size in stock_data[sku_id]:
                size = size.split('/')[0]
                if stock_data[sku_id][size] == 'lieferbar innerhalb 3 Wochen':
                    product['skus'][self.stock_counter].update({'out_of_stock': True})
                self.stock_counter = self.stock_counter + 1

        return self.parse_additional_requests(requests, product)

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
        categories = self.product_category(response)
        product['category'] = categories
        trails = self.product_trail(response)

        category_counter = 0
        trail_list = []

        for trail in trails:
            trail_list.append((categories[category_counter], trail))
            category_counter = category_counter + 1
        product['trail'] = trail_list

        for category in categories:
            if category in self.gender_dict:
                product['gender'] = self.gender_dict[category]
            else:
                product['gender'] = None

        product['skus'] = self.product_skus(response)
        product['care'] = self.product_care(response)

        if not product['gender']:
            product['industry'] = "Homeware"

        product['merch_info'] = self.product_merch_info(response)

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

        for size in sizes:
            sku = {}
            sku["size"] = size
            sku["price"] = self.product_price(response)
            sku["currency"] = self.product_currency(response)
            sku["color"] = self.product_color(response)
            id = self.product_retailer_sku(response)
            sku["sku_id"] = id + '|' + sku['color'] + '|' + sku['size'] + '|' + sku['price']
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

        for request_url in addl_colors_urls:
            additional_requests += self.out_of_stock_request(response)
            additional_requests.append(Request(url=request_url, callback=self.parse_extra_images, dont_filter=True))

        return additional_requests

    def parse_extra_images(self, response):
        product = response.meta['product']
        requests = response.meta['requests']
        product['skus'].update(self.product_skus(response))
        product['images_urls'] += self.product_images(response)
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
        brand = response.css('meta.at-dv-brand::attr(content)').extract_first()
        return brand

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
        currency = response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()
        return currency

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
        id = response.css('.js-current-artnum::attr(value)').extract_first()
        return id

    @staticmethod
    def product_description(response):
        desc = response.css('div.l-outsp-bot-10 li::text').extract()
        return clean_product(desc)

    @staticmethod
    def product_url_origin(response):
        url_origin = response.css('link[rel="canonical"]::attr(href)').extract_first()
        return url_origin

    @staticmethod
    def product_trail(response):
        trails = response.css('div#breadcrumb li>a::attr(href)').extract()
        return trails

    @staticmethod
    def product_category(response):
        category_list = response.css('div#breadcrumb a>span::text').extract()
        return category_list

    @staticmethod
    def product_color(response):
        color = response.css('.js-current-color-name::attr(value)').re_first(r'(\w+)')
        return color

    @staticmethod
    def product_size(response):
        sizes = response.css('.js-sizeSelector button::text').re(r'(\d+)')
        return sizes

    @staticmethod
    def product_merch_info(response):
        return None


def clean_product(raw_data):
    cleaned_list = []
    for item in raw_data:
        item = item.strip()
        if item:
            cleaned_list.append(item)
    return cleaned_list
