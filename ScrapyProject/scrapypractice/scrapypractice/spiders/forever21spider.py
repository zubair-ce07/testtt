import scrapy
import json

from scrapy import Request
from scrapy import Selector

from scrapypractice.items import ProductItem, VariationItem, SizeItem


class ForeverSpider(scrapy.Spider):
    name = 'forever21spider'

    products_url = 'https://www.forever21.com/us/shop/Catalog/GetProducts'
    payload = {
        "page": {"pageNo": "1", "pageSize": "20000"},
        "filter": {
            "sizeList": [],
            "colorList": [],
            "price": {"minPrice": 0, "maxPrice": 15000},
            "manualList": [],
            "filterData": {}},
        "sort": {"sortType": ""},
        "count": {"products": ""},
        "soldout": {
            "Brand": "",
            "DisplayName": "",
            "ListPrice": "",
            "ProductId": "",
            "Variants": [],
            "selectedColorNameOOS": "",
            "selectedColorOOS": "",
            "selectedSizeNameOOS": "",
            "selectedSizeOOS": "",
            "colorObj": ""},
        "landing": {},
        "loopCount": 0
    }
    start_urls = [
        'https://www.forever21.com/us/shop'
    ]
    rotate_user_agent = True

    def parse(self, response):
        category_urls = response.xpath("//div[@class='table sameline full t_futura_light hide_tablecell_mobile "
                                       "hide_tablecell_tablet pl_20']/div/div/div/div[1]/div/div/p/a/@href").extract()

        header = {'content-type': 'application/json'}
        for category_url in category_urls:
            brand, category = category_url.split('/')[-2:]
            self.payload['brand'] = brand
            self.payload['category'] = category

            if brand != 'giftcard':
                yield Request(
                    url=self.products_url,
                    callback=self.parse_category,
                    headers=header,
                    method='POST',
                    body=json.dumps(self.payload),
                )

    def parse_category(self, response):
        try:
            products = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            products = dict()
            pass

        for product in products.get('CatalogProducts', []):
            meta = {'product': product}
            yield Request(
                url=product['ProductShareLinkUrl'],
                callback=self.parse_product,
                meta=meta,
            )

    def parse_product(self, response):
        product_item = self.product_info(response.meta['product'])
        yield product_item

    def product_info(self, product_details):
        description_html = product_details['Description']
        description = Selector(text=description_html).xpath('//div[@class="d_content"]/text()').extract_first()

        product_item = ProductItem(
            product_url=product_details['ProductShareLinkUrl'],
            store_keeping_unit=product_details['ProductId'],
            title=product_details['DisplayName'],
            brand=product_details['Brand'],
            locale='en_US',
            currency='USD',
            variations=self.variation_info(product_details),
            description=description,
        )

        return product_item

    def variation_info(self, product_details):
        variation_item_list = []
        for color in product_details['Variants']:
            variation_item = VariationItem(
                display_color_name=color['ColorName'],
                images_urls=color['ImageFileName'],
                sizes=self.size_info(color),
            )
            variation_item_list.append(variation_item)

        return variation_item_list

    def size_info(self, color_details):
        size_items_list = []

        for size in color_details['Sizes']:
            is_discounted = False if color_details['OriginalPrice'] - color_details['ListPrice'] == 0 else True
            size_item = SizeItem(
                size_name=size['SizeName'],
                is_available=size['Available'],
                price=color_details['OriginalPrice'],
                is_discounted=is_discounted,
                discounted_price=color_details['ListPrice'] if is_discounted else '',
            )
            size_items_list.append(size_item)

        return size_items_list
