import json
import re
import urllib
import urllib.parse as urlparse

from parsel import Selector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from sears_scraper.items import SearsItem


def process_layout_link(value):
    return value.replace("chrono.shld.net/", "www.sears.com/")


class SearsSpider(CrawlSpider):
    name = "sears"
    allowed_domains = ["sears.com", "chrono.shld.net"]
    start_urls = ["http://chrono.shld.net/segments/sears-us-hdrv3-flyouts.html?v=107"]

    store_id = '10153'
    catalog_id = '12605'

    product_search_url = "http://www.sears.com/service/search/productSearch"
    product_url = "http://www.sears.com/content/pdp/config/products/v1/products/{}?site=sears"
    variant_price_url = "http://www.sears.com/content/pdp/products/pricing/v2/get/price/display/json?"\
                        "priceMatch=Y&memberType=G&urgencyDeal=Y&site=SEARS&offer="
    products_hierarchy_url = "http://www.sears.com/browse/services/v1/hierarchy/fetch-paths-by-id/{}?" \
                             "clientId=obusearch&\site=sears"

    rules = (
        Rule(LinkExtractor(allow=['/clothing'], deny=['/articles', 'filterList='], process_value=process_layout_link),
             callback="parse_categories", follow=True),
    )

    def parse_categories(self, response):
        cat_group_id = re.findall('/b-(\d+)', response.url)

        if cat_group_id:
            url = self.products_hierarchy_url.format(cat_group_id[0])
            yield Request(url, callback=self.parse_products_api,
                          meta={'cat_group_id': cat_group_id[0]})

    def parse_products_api(self, response):
        json_response = json.loads(response.body)
        json_response = json_response['data'][0]

        catgroup_id = json_response['catgroupId']
        catgroup_id_path = json_response['catgroups'][0]['idPath']
        name_path = urllib.parse.quote_plus(json_response['catgroups'][0]['namePath'])
        url = "http://www.sears.com/service/search/productSearch"
        params = {
            'pageNum': 1,
            'catalogId': self.catalog_id,
            'catgroupId': catgroup_id,
            'catgroupIdPath': catgroup_id_path,
            'levels': urlparse.unquote_plus(name_path),
            'primaryPath': urlparse.unquote_plus(name_path),
            'storeId': self.store_id,
            'searchBy': 'subcategory',
            'tabClicked': 'All',
        }
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)

        url_parts[4] = urllib.parse.urlencode(query)
        complete_url = urlparse.urlunparse(url_parts)

        return Request(complete_url, callback=self.parse_products_data)

    def parse_products_data(self, response):
        json_data = json.loads(response.body)['data']

        for product_data in json_data['products']:
            yield self.get_product_data_request(
                product_data['sin'],
                {"url": product_data['url']})

        next_page_num = 'pageNum={}'.format(json_data['currentPageNumber'] + 1)
        current_page = 'pageNum={}'.format(json_data['currentPageNumber'])

        if json_data['pageEnd'] != json_data['productCount']:
            url = response.url.replace(current_page, next_page_num)
            yield Request(url, callback=self.parse_products_data)

    def get_product_data_request(self, prod_sin, meta):
        url = self.product_url.format(prod_sin)
        return Request(url, callback=self.parse_apparel_item, meta=meta)

    def parse_apparel_item(self, response):
        response_data = json.loads(response.body)['data']
        product_data = response_data['product']

        apparel_item = SearsItem()
        retailer_sku = self.get_retailer_sku(response_data)
        if not retailer_sku:
            return

        apparel_item['retailer_sku'] = retailer_sku
        apparel_item['name'] = self.get_name(product_data)
        apparel_item['brand'] = self.get_brand_name(product_data)
        apparel_item['image_urls'] = self.get_image_urls(product_data)
        apparel_item['desc'] = self.get_item_description(product_data)
        apparel_item['url'] = self.get_item_url(response)

        web_paths = response_data["productmapping"]["primaryWebPath"]
        apparel_item['category'] = self.get_category(web_paths)
        apparel_item['gender'] = self.get_gender(web_paths)

        skus, sku_ids = self.get_sku_info(response_data)
        if sku_ids:
            return self.get_sku_request(sku_ids, skus, apparel_item)
        else:
            apparel_item['skus'] = skus or {'sku': 'one-size'}
            return apparel_item

    def get_gender(self, web_paths):
        if [web_path for web_path in web_paths if 'Men\'s' in web_path['name']]:
            return "male"
        elif [web_path for web_path in web_paths if 'Women\'s' in web_path['name']]:
            return "female"

        return "baby"

    def get_name(self, product_data):
        return product_data['name']

    def get_retailer_sku(self, response_data):
        return response_data['productstatus'].get('ssin')

    def get_brand_name(self, product_data):
        return product_data.get('brand', {}).get('name', 'Sears')

    def get_image_urls(self, product_data):
        image_urls = []
        for img_assets in product_data['assets']['imgs']:
            images = [image['src'] for image in
                      img_assets.get('vals', []) if image.get('src')]
            image_urls.extend(images)
        return image_urls

    def get_category(self, web_paths):
        last_web_path = max(web_paths, key=lambda web_path: web_path['level'])
        return last_web_path.get('name', 'N/A')

    def get_item_description(self, product_data):
        item_desc = []
        tags = 'li::text, p::text, strong::text'
        for desc in product_data['desc']:
            sel = Selector(text=desc['val'])
            desc_points = sel.css(tags).extract()
            item_desc.extend(desc_points)

        return self.clean_object(item_desc)

    def get_item_url(self, response):
        return urlparse.urljoin('http://sears.com', response.meta['url'])

    def get_sku_info(self, response_data):
        prod_attrs = response_data.get('attributes', {}).get('variants',[])

        skus = {}
        sku_ids = []
        for attr in prod_attrs:
            size_elems = []
            color = []
            for elem in attr['attributes']:
                if elem['name'] == "Color":
                    color.append(elem['value'])
                else:
                    size_elems.append(elem['value'])

            size = '-'.join(size_elems)
            color = color or []

            default_sku_id = size + color[0]
            sku_id = attr.get('offerId', default_sku_id)
            sku = {
                'currency': 'USD',
                'size': size,
            }

            if color:
                sku['color'] = color

            skus[sku_id] = sku
            if sku_id is not default_sku_id:
                sku_ids.append(sku_id)

        return skus, sku_ids

    def parse_sku_price(self, response):
        item = response.meta['item']
        skus = response.meta['skus']
        sku_ids = response.meta['sku_ids']
        req_sku_id = response.meta['req_sku_id']

        json_data = json.loads(response.body)
        prices = json_data['priceDisplay']['response'][0]['prices']

        skus[req_sku_id]['price'] = prices['finalPrice']['max']
        skus[req_sku_id]['previous_prices'] = prices['regularPrice']['max']

        if sku_ids:
            return self.get_sku_request(sku_ids, skus, item)
        else:
            item['skus'] = skus
            return item

    def get_sku_request(self, sku_ids, skus, item):
        first_sku = sku_ids.pop(0)
        meta = {'skus': skus,
                'sku_ids': sku_ids,
                'req_sku_id': first_sku,
                'item': item}
        return Request(self.variant_price_url + first_sku,
                       callback=self.parse_sku_price,
                       headers={'AuthID': 'aA0NvvAIrVJY0vXTc99mQQ=='},
                       meta=meta,)

    def clean_object(self, obj):
        clean_obj = [x.strip('\t\n ') for x in obj]
        return [x for x in clean_obj if x]
