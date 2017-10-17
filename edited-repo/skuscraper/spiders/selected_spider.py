import re

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, CurrencyParser, clean


class Mixin:
    retailer = 'selected-cn'
    allowed_domains = ['selected.com.cn']
    lang = 'zh'
    market = 'CN'
    brand_map = {'男士': 'Selected Homme', '女': 'Selected Femme'}
    page_size = 40
    pagination_base_url = ("http://www.selected.com.cn/webapp/wcs/stores/servlet/CategoryNavigationResultsView?manufac"
                           "turer=&searchType=&resultCatEntryType=&searchTerm=+&catalogId=10001&categoryId=-{gender_id}"
                           "&storeId=10151&metaData==&pageSize=40&beginIndex={starting_index}&orderBy=5&categoryId=")
    start_urls_with_meta = [
        ('http://www.selected.com.cn/cn/sltstore/quanbunanzhuang.html', {'gender': 'men'}),
        ('http://www.selected.com.cn/cn/sltstore/quanbunvzhuang.html', {'gender': 'women'}),
    ]


class SelectedParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['skus'] = self.product_skus(response)
        garment['image_urls'] = self.product_image_urls(response)
        return garment

    def product_image_urls(self, response):
        img_urls = clean(response.css('.smallImg img::attr(src)'))
        if not img_urls:
            return
        urls = []
        color_codes = self.color_codes(response)
        for code in color_codes:
            if code in img_urls[0]:
                active_color_code = code
        for code in color_codes:
            if code is active_color_code:
                continue
            copies_urls = img_urls.copy()
            copies_urls = [u.replace(active_color_code, code) for u in copies_urls]
            urls.extend(copies_urls)
        return img_urls + urls

    def product_skus(self, response):
        skus = {}
        curreny = self.curreny(response)
        for color, c_code in zip(self.product_colors(response), self.color_codes(response)):
            for size in self.product_sizes(response, c_code):
                sku = {}
                sku['color'] = color
                sku['currency'] = curreny
                sku['price'] = self.product_price(response, c_code)
                sku['size'] = size
                skus[color + size] = sku
        return skus

    def color_codes(self, response):
        return clean(response.css('.pPropColor a::attr("cpartnumber")'))

    def product_care(self, response):
        description, care, delivery_note = clean(response.css('.menu_body::text'))
        return care

    def product_colors(self, response):
        return clean(response.css('.pPropColor img::attr("title")'))

    def product_price(self, response, c_code):
        price = clean(response.css('.pRightPice div[id*="{}"] strong::text'.format(c_code)))[0]
        return int(''.join(re.findall('\d+', price)))

    def product_sizes(self, response, c_code):
        size_quantity = clean(response.css('div[id*="{}"] input::attr(value)'.format(c_code)))
        sizes = clean(response.css('div[id*="{}"] a::text'.format(c_code)))
        return [size for size, quantity in zip(sizes, size_quantity) if quantity != "0.0"]

    def product_category(self, response):
        return clean(response.css('.productListGroup a::text'))[1:]

    def product_id(self, response):
        id = clean(response.css('.c-gray6:not([id])::text'))[0]
        return ''.join(re.findall('\d+', id))

    def product_name(self, response):
        return clean(response.css('.popProDelRight h3::text'))[0]

    def product_description(self, response):
        description, care, delivery_note = clean(response.css('.menu_body::text'))
        return description

    def product_brand(self, response):
        product_name = self.product_name(response)
        for brand_str, brand in self.brand_map.items():
            if brand_str in product_name:
                return brand
        return 'Selected'

    def curreny(self, response):
        return CurrencyParser.currency(clean(response.css('.pRightPice div[id="div_price"] strong::text'))[0])


class SelectedCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = SelectedParseSpider()

    products_css = '.pageContainerList'

    def parse(self, response):
        yield from super(SelectedCrawlSpider, self).parse(response)

        current_page = int(clean(response.css('.pageNumbers .listFbfeetFix ::text'))[0])
        last_page = int(clean(response.css('.listFbfeet li:nth-last-child(2) a::text'))[0])
        if current_page == last_page:
            return
        gender = response.meta['gender']
        g_id = 40 if gender == 'men' else 41
        url = self.pagination_base_url.format(starting_index=current_page * self.page_size, gender_id=g_id)
        yield Request(url, meta=response.meta, callback=self.parse)

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
