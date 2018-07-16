import scrapy
import json
from urllib.parse import urlparse


class ProductsSpider(scrapy.Spider):
    name = 'jacklemkus'
    start_urls = ['https://www.jacklemkus.com/sneakers?p=1',
                  'https://www.jacklemkus.com/mens-apparel?p=1',
                  'https://www.jacklemkus.com/womens-apparel?p=1',
                  'https://www.jacklemkus.com/accessories?p=1',
                  'https://www.jacklemkus.com/kids?p=1'
                  ]

    def parse(self, response):

        for href in response.css('ol.row a.product-image::attr(href)'):
            yield response.follow(href, self.parse_product)
        page_query = 'div.js-infinite-scroll-pager-data::attr({})'

        current_page = response.css(page_query.format('data-currentpage')).extract_first()
        last_page = response.css(page_query.format('data-lastpage')).extract_first()

        if current_page is not last_page:
            next_url = '?p={}'.format(int(current_page) + 1)
            yield response.follow(next_url, self.parse)

    def parse_product(self, response):

        def extract_with_css(query):
            return response.css(query)

        def extract_with_xpath(query):
            path = "//body//div[@class='row']" \
                   "//tbody//th[contains(.,'{}')]/following-sibling::td/text()".format(query)

            return response.xpath(path)

        def get_category():
            base_url = urlparse(response.request.headers.get('Referer', None).decode("utf-8"))
            categories = extract_with_xpath('DEPARTMENT').extract().append(base_url.path[1:])
            product_type = extract_with_xpath('Type').extract()
            return categories + product_type

        def get_brand():
            selector = extract_with_xpath('Brand').extract_first()
            return "local" if selector is None else selector.strip()

        def get_gender():
            selector = extract_with_xpath('Gender').extract_first()
            return "None" if selector is None else selector.strip()

        def get_list_of_skus():
            lookup_mine = json.loads(response.css('div.product-data-mine::attr(data-lookup)')
                                     .extract_first().replace("\'", "\""))
            list_of_sku = []
            for item in lookup_mine.values():
                product_sku = {}
                price = response.css('div.product-essential span.price::text').extract_first()
                if price[0] is 'R':
                    product_sku["price"] = float(price[1:].replace(",", ""))
                    product_sku["currency"] = 'RAND'
                product_sku["size"] = item.get("size")
                product_sku["sku_id"] = "{}_{}".format(item.get("id"),
                                                       item.get("size").replace(" ", '_'))
                if not item.get("stock_status"):
                    product_sku["out_of_stock"] = True
                list_of_sku.append(product_sku)
            return list_of_sku

        yield {
            'retailer_sku': extract_with_css(
                'div.product-essential span.sku::text').extract_first().strip(),

            'gender': get_gender(),
            'category': get_category(),
            'brand': get_brand(),
            'url': response.url,
            'name': extract_with_css(
                'div.product-essential div.product-name h1::text').extract_first().strip(),

            'description': [extract_with_css('div.row div.std::text').extract_first().strip()],
            'image_urls': extract_with_css(
                'div.product-essential p.product-image a::attr(href)').extract(),
            'suks': get_list_of_skus()
        }
