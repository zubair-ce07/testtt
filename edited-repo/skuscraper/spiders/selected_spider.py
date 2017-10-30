import re

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'selected-cn'
    allowed_domains = ['selected.com.cn']
    lang = 'zh'
    market = 'CN'
    page_size = 40
    url_regex = 'url = "(.+)";'
    pagination_base_url = "=&pageSize=40&beginIndex={starting_index}&orderBy=5&categoryId="
    image_url_t = "http://img1.selected.com.cn/slt/product/{p_id}/{c_code}/{c_code}{i_name}"
    start_urls_with_meta = [
        ('http://www.selected.com.cn/cn/sltstore/quanbunanzhuang.html', {'gender': 'men'}),
        ('http://www.selected.com.cn/cn/sltstore/quanbunvzhuang.html', {'gender': 'women'}),
    ]


class SelectedParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.pRightPice[id="div_price"] ::text'

    def parse(self, response):
        p_id = self.product_id(response)
        garment = self.new_unique_garment(p_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.product_image_urls(response)
        return garment

    def product_image_urls(self, response):
        img_names = clean(response.css('.smallImg img::attr(name)'))
        if not img_names:
            return []
        image_urls = []
        color_codes = self.color_codes(response)
        p_id = self.product_id(response)
        for code in color_codes:
            for name in img_names:
                image_urls.append(self.image_url_t.format(p_id=p_id, c_code=code, i_name=name))
        return image_urls

    def skus(self, response):
        skus = {}
        common = self.product_pricing_common_new(response)
        for colour_s in response.css('.pPropColor li'):
            colour = clean(colour_s.css('img ::attr(title)'))[0]
            colour_code = clean(colour_s.css('a ::attr(cpartnumber)'))[0]
            common['colour'] = colour
            for size_s in response.css(".popPageSel div[id*='{}'] a ".format(colour_code)):
                sku = common.copy()
                size = clean(size_s.css(' a::text'))[0]
                sku['size'] = size
                if size_s.css('input[value="0.0"]'):
                    sku['out_of_stock'] = True
                skus['{}_{}'.format(colour, size)] = sku
        return skus

    def color_codes(self, response):
        return clean(response.css('.pPropColor a::attr("cpartnumber")'))

    def product_care(self, response):
        return clean(response.xpath('//div[@class="menu_list"]/div[@class="menu_body"][2]/text()'))

    def product_category(self, response):
        return clean(response.css('.productListGroup a::text'))[1:]

    def product_id(self, response):
        p_id = clean(response.css('.c-gray6:not([id])::text'))[0]
        return p_id.split(": ")[1]

    def product_name(self, response):
        return clean(response.css('.popProDelRight h3::text'))[0]

    def product_description(self, response):
        return clean(response.xpath('//div[@class="menu_list"]/div[@class="menu_body"][1]/text()'))

    def product_brand(self, response):
        gender = response.meta['gender']
        return 'Selected Homme' if gender is 'men' else 'Selected Femme'


class SelectedCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = SelectedParseSpider()
    products_css = '.pageContainerList'

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse(self, response):
        yield from super(SelectedCrawlSpider, self).parse(response)

        current_page = int(clean(response.css('.pageNumbers .listFbfeetFix ::text'))[0])
        last_page = int(clean(response.css('.listFbfeet li:nth-last-child(2) a::text'))[0])
        if current_page == last_page:
            return
        base_url = response.xpath('//script[contains(text(),"pageSize")]').re(self.url_regex)[0]
        pagination_url = self.pagination_base_url.format(starting_index=current_page * self.page_size)
        response.meta['trail'] = self.add_trail(response)
        yield Request(base_url + pagination_url, meta=response.meta, callback=self.parse)
