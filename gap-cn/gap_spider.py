import json

from scrapy import Request
from scrapy import Selector
from scrapy.http.request.form import FormRequest
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'gap-cn'
    lang = 'CN'
    market = 'CN'
    allowed_domains = ['gap.cn']
    start_urls = ['http://www.gap.cn/category/25.html']


class GapParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    gender_map = [
        ('女装', 'women'),
        ('孕妇装', 'women'),
        ('男装', 'men'),
        ('男孩', 'boys'),
        ('女孩', 'girls'),
        ('女幼', 'girls'),
        ('婴儿', 'unisex-kids'),
        ('男幼', 'unisex-kids'),
    ]

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(garment)
        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)
        request_queue = [self.stock_request(garment),
                         self.merch_info_request(garment)]

        garment['meta']={
            'requests_queue': request_queue,
        }

        return self.next_request_or_garment(garment)

    def parse_stock_info(self, response):
        stock_info = json.loads(response.text)
        garment = response.meta['garment']
        skus = garment['skus']
        for sku in skus:
            if not stock_info[sku]:
                skus[sku].update({'out_of_stock': True})

        return self.next_request_or_garment(garment)

    def parse_merch_info(self, response):
        merch_info = json.loads(response.text)
        if merch_info:
            garment = response.meta['garment']
            sku_id = garment['retailer_sku']
            info = merch_info.get(sku_id)
            if info:
                garment['merch_info'] = [i['label'] for i in info]
        return self.next_request_or_garment(garment)

    def stock_request(self, garment):
        entity_id = str(garment['retailer_sku'])
        stock_url = 'http://www.gap.cn/catalog/product/getstock?entityId='+ entity_id
        return Request(url=stock_url, callback=self.parse_stock_info)

    def merch_info_request(self, garment):
        entity_id = str(garment['retailer_sku'])
        merch_info_url = 'http://www.gap.cn/catalog/product/prom'
        formdata = {
            'ids[]': entity_id
        }
        return FormRequest(url=merch_info_url,
                           formdata=formdata,
                           callback=self.parse_merch_info)


    def product_id(self, response):
        css = 'input[name=product]::attr(value)'
        return int(response.css(css).extract_first())

    def product_gender(self, garment):
        categories = [c for c in garment['category']]

        for text, gender in self.gender_map:
            if text in categories:
                return gender

    def skus(self, response):
        colors = self.product_colors(response)
        sku_data = [(color, self.get_color_sizes(response, color['key']))
                    for color in colors]
        skus = {}
        for color, sizes in sku_data:
            for size in sizes:
                skuid = size['sku']
                sku = {
                    'size': size['title'],
                    'color': color['title'],
                    'price': self.format_price(size['final_price']),
                    'currency': color['currency'],
                }
                if not (size['final_price'] == size['price']):
                    prev_price = self.format_price(size['price'])
                    sku.update({'previous_price': prev_price})

                skus[skuid] = sku

        return skus

    def get_color_sizes(self, response, color_key):
        elems = response.css('span.size_options_entity_' + color_key + ' a')
        return [
            {
                'title': self.get_attr(elem, 'title'),
                'sku': self.get_attr(elem, 'id').split('_')[-1],
                'price': self.get_attr(elem, 'price'),
                'final_price': self.get_attr(elem, 'final_price'),
            } for elem in elems
        ]

    def product_colors(self, response):
        elems = response.css('#color_options_list  a')
        currency_re = 'money\(\'.*?\',.*,\'(.*?)\'\)'
        return [
            {
                'title': self.get_attr(elem, 'title'),
                'key': self.get_attr(elem, 'key'),
                'currency': elem.css('::attr(onclick)').re_first(currency_re),
            } for elem in elems
        ]

    def product_brand(self, hxs):
        return 'gap'

    def product_name(self, response):
        name_css = 'div.product-name > div:first-child::text'
        return response.css(name_css).extract_first()

    def product_description(self, response):
        css = 'meta[name=description]::attr(content)'
        return response.css(css).extract()

    def product_care(self, response):
        info_table = response.css('#product_disc table').extract_first()
        cells = Selector(text=info_table).css('td::text').extract()
        care_criteria = [
            '面料',  # fabric
            '棉',  # cotton
            '聚酯',  # polyester
            '纤',  # fiber
            '干',  # dry
            '熨',  # iron
            '%',  # %
        ]

        return [x for x in cells if any(criteria in x for criteria in care_criteria)]

    def image_urls(self, response):
        css = 'ul.more-views a::attr(href)'
        return response.css(css).extract()

    def product_category(self, response):
        return response.css('div.breadcrumbs a::text').extract()

    def format_price(self, price_raw):
        return int(price_raw.replace('.',''))

    def get_attr(self, elem, attr):
        return elem.css('::attr('+attr+')').extract_first()


class GapCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = GapParseSpider()

    product_css = ['.categoryProductItem']
    listing_css = ['.sidebar']
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_listing'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css='#navs')),
    )

    def parse_listing(self, response):        
        for request in self.ajax_requests(response):
            yield request
        
        for request in self.requests_from_ids(response): 
            yield request

        return super(GapCrawlSpider, self).parse(response)

    def parse_ajax_response(self, response):
        result = json.loads(response.text)
        if result['status'] == 'success':
            page_segment = result['message']
            ajax_response = Response(url=response.url,
                                     body=str.encode(page_segment))
            return super(GapCrawlSpider, self).parse(ajax_response)
    
    def ajax_requests(self, response):
        all_cat_css = '#allCategoryId::attr(value)'
        all_category_ids = response.css(all_cat_css).extract_first()
        last_cat_css = '#product_list_184 .clear'
        last_category_clear = response.css(last_cat_css)[-1]
        last_cat_id_css = '::attr(currentcategoryid)'
        last_category_id = last_category_clear.css(last_cat_id_css).extract_first()
        if last_category_id:
            all_prod_id_css = '::attr(allproductids' + last_category_id + ')'
            all_product_ids = last_category_clear.css(all_prod_id_css).extract_first() \
                .rstrip(',').split(',')
            curr_displayed_css = '::attr(currentcategorydisplaynum' + last_category_id + ')'
            current_displayed = int(last_category_clear.css(curr_displayed_css).extract_first())
            last_cat_items_css = '::attr(currentcategorytotalnum)'
            last_category_total_items = int(last_category_clear.css(last_cat_items_css).extract_first())
            curr_page_css = '::attr(currentpage)'
            current_page = last_category_clear.css(curr_page_css).extract_first()
            categories_displayed = ''
            last_category_display_num = 0
            product_ids = ''
            clear_css = '#product_list_184 .clear'
            clear_elems = response.css(clear_css)
            cat_id_css = '::attr(currentcategoryid)'
            curr_cat_disp_css = '::attr(currentcategorydisplaynum' + last_category_id + ')'
            for elem in clear_elems:
                if elem.css(cat_id_css):
                    categories_displayed += elem.css(cat_id_css).extract_first() + ','
                if elem.css(curr_cat_disp_css):
                    last_category_display_num += int(elem.css(curr_cat_disp_css).extract_first())
                    product_ids += elem.css(all_prod_id_css).extract_first()
            if current_displayed < last_category_total_items:
                # Send ajax request for more items
                formdata = {
                    'allCategoryId': all_category_ids,
                    'currentPage': current_page,
                    'haveDisplayAllCategoryId': categories_displayed,
                    'lastCategoryDisplayNum': str(last_category_display_num),
                    'lastCategoryId': last_category_id,
                    'lastCategoryTotalNum': str(last_category_total_items),
                    'productIds': product_ids,
                }
                catalog_url = '/catalog/category/getCategoryProduct'
                yield FormRequest(url=response.urljoin(catalog_url), formdata=formdata,
                                  callback=self.parse_ajax_response)
                
    def request_from_ids(self, response):
        categories_css = '#product_list_184 .clear::attr(currentcategoryid)'
        category_ids = response.css(categories_css)
        if category_ids:
            for category in category_ids:
                category_id = category.extract()
                css = '::attr(allproductids' + category_id + ')'
                ids = response.css(css).extract_first().rstrip(',')
                for id in ids:
                    url_segment = '/category/' + category_id + '/product/' + id + '.html'
                    yield Request(url=response.urljoin(url_segment))
