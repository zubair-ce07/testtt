import json
import re
import scrapy
from scrapy.spiders import CrawlSpider


def clean(raw_strs):
    if isinstance(raw_strs, list):
        cleaned_strs = [re.sub('\s+', ' ', st).strip() for st in raw_strs]
        return [st for st in cleaned_strs if st]
    elif isinstance(raw_strs, str):
        return re.sub('\s+', ' ', raw_strs).strip()


class GapItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()


class Gap(CrawlSpider):
    name = 'gap'
    allowed_domains = ['gap.cn']
    api_url = 'https://www.gap.cn/gap/rest/category?'
    listing_url_t = '{}cid={}'
    catg_url_t = '{}id={}'
    product_url_t = 'https://www.gap.cn/gap/rest/productnew?id={}&store_id=1&customer_group_id=0'
    product_page_url_t = '{}cid={}&store_id=1&from=side&customer_group_id=0'
    pagination_url_t = 'https://www.gap.cn/gap/rest/category?cid={}&action=getCategoryProduct&page={}&store_' \
                       'id=1&platform=pc&allCategoryId={}&lastCategoryId={}&lastCategoryDisplayNum={}' \
                       '&lastCategoryTotalNum={}&haveDisplayAllCategoryId={}&from=side&customer_group_id=0'
    products_url_t = 'https://www.gap.cn/gap/rest/category?cid={}&store_id=1&from=side&customer_group_id=0'
    gender_dict = {
        '孕妇装|': 'women',
        '女装|': 'women',
        '男装|': 'men',
        '女孩|': 'girl',
        '男孩|': 'boy',
        '幼儿|': 'unisex-kids',
        '婴儿|': 'unisex-kids'
    }
    start_urls = [
        'https://www.gap.cn/gap/rest/category?action=getTopNavs&store_id=1'
    ]

    def parse(self, response):
        listings_json = json.loads(response.text)['data']['marketTopNavs']
        return [response.follow(self.listing_url_t.format(self.api_url, listing_id.get("id")),
                                callback=self.parse_categories)
                for listing_id in listings_json]

    def parse_categories(self, response):
        categories_json = json.loads(response.text)['data']['currentProductList']['currentChildCategoryIdAll']
        return [response.follow(self.catg_url_t.format(self.api_url, category_code),
                                callback=self.parse_subcategories)
                for category_code in categories_json.split(',')]

    def parse_subcategories(self, response):
        subcategories_json = json.loads(response.text)['data']['child_categories']
        return [response.follow(self.products_url_t.format(subcategory_code), callback=self.parse_pagination,
                                meta={'catg_id': subcategory_code}) for subcategory_code in subcategories_json]

    def parse_pagination(self, response):
        catg_id = response.meta['catg_id']
        products_json = json.loads(response.text)
        total_products = int(products_json['data']['currentProductList']['categoryProducts'
                                                                         '']['category_' + catg_id]['category'
                                                                                                    '']['product_count'])
        page_number = 1
        return [response.follow(self.pagination_url_t.format(catg_id, page_number, catg_id, catg_id,
                                                             product_displayed, total_products, catg_id),
                                callback=self.parse_products, meta={'catg_id': catg_id})
                for product_displayed in range(0, total_products, 60)]

    def parse_products(self, response):
        catg_id = response.meta['catg_id']
        products_json = json.loads(response.text)['data']['categoryProducts']
        return [
            response.follow(self.product_url_t.format(product_code['productId']),
                            callback=self.parse_item)
            for product_code in
            products_json['category_' + catg_id]['products']]

    def parse_item(self, response):
        raw_product = json.loads(response.text)
        item = GapItem()
        item['retailer_sku'] = self.retailer_sku(raw_product)
        item['gender'] = self.product_gender(raw_product)
        item['name'] = self.product_name(raw_product)
        item['category'] = self.product_category(raw_product)
        item['url'] = self.product_url(raw_product)
        item['brand'] = self.product_brand(raw_product)
        item['description'] = self.product_description(raw_product)
        item['care'] = self.product_care(raw_product)
        item['image_urls'] = self.images_url(raw_product)
        item['skus'] = self.parse_sku(raw_product)
        return item

    def retailer_sku(self, raw_product):
        return raw_product['data']['trackingcode']['productId']

    def product_gender(self, raw_product):
        return self.gender_dict.get(raw_product.get('data').get('prefixCategoryName'), 'unisex-adults')

    def product_name(self, raw_product):
        return raw_product.get('data').get('productName')

    def product_category(self, raw_product):
        return raw_product.get('data').get('categoriesName')

    def product_url(self, raw_product):
        return raw_product.get('data').get('shareUrl')

    def product_brand(self, raw_product):
        return raw_product.get('data').get('trackingcode').get('dps360_brand')

    def product_description(self, raw_product):
        return clean(raw_product.get('data').get('productDetail').get('productFiber'))

    def product_care(self, raw_product):
        return clean(raw_product.get('data').get('productDetail').get('productCare'))

    def images_url(self, raw_product):
        return [image_list.get('productImageUrl')
                for image_list in raw_product.get('data').get('imageList')]

    def parse_sku(self, raw_product):
        sku = {}
        for color_json in raw_product.get('data').get('colors'):
            color = color_json.get("colorName")
            for size in color_json.get('size'):
                size = size.get("sizeNumber")
                sku.update({
                    f'{color}_{size}': {
                        'size': size,
                        'color': color,
                        'sale_price': color_json.get("salePrice"),
                        'price': color_json.get("price")
                    }
                })
        return sku

