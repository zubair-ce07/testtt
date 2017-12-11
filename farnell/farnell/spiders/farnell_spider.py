import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import FarnellItem


class FarnellSpider(CrawlSpider):
    name = 'farnell-uk'
    start_urls = [
        'http://uk.farnell.com/c/engineering-software',
        'http://uk.farnell.com/c/electrical',
        'http://uk.farnell.com/c/wireless-modules-adaptors',
    ]
    allowed_domains = ['uk.farnell.com', ]
    rules = [
        Rule(LinkExtractor(restrict_css='.filterCategoryLevelOne')),
        Rule(LinkExtractor(restrict_css='.bottomPa .paginNextArrow')),
        Rule(LinkExtractor(restrict_css='.productImage'), callback='parse_item'),
    ]

    def parse_item(self, response):
        product = FarnellItem()
        product['url'] = response.url
        product['unit_price'] = self.product_price(response)
        product['information'] = self.product_information(response)
        product['title'] = self.product_title(response)
        product['brand'] = self.product_brand(response)
        product['overview'] = self.product_overview(response)
        product['manufacturer'] = self.product_manufacturer(response)
        product['manufacturer_part'] = self.product_manufacturer_part(response)
        product['files'], product['file_urls'] = self.product_files(response)
        product['primary_image_url'] = self.product_primary_img_url(response)
        product['tariff_number'] = self.product_tariff_num(response)
        product['origin_country'] = self.product_origin_country(response)
        product['trail'] = self.product_trail(response)
        return product

    def product_price(self, response):
        price_str = "".join(self.clean(response.css('.productPrice .price::text').re('\d+.+')))
        if not price_str:
            return price_str
        return float(re.sub(',', '', price_str))

    def product_title(self, response):
        title_selector = response.css('section[aria-label="Product Image And Description"]')
        p_title = self.clean(title_selector.css('h1::text').extract_first())
        return p_title + self.clean(title_selector.css('span::text').extract_first())

    def product_information(self, response):
        information = []
        info_name_selector = response.css('section[aria-label="Product Information"] dt')
        info_value_selector = response.css('section[aria-label="Product Information"] dd')
        for n_selector, v_selector in zip(info_name_selector, info_value_selector):
            info_map = {}
            info_map['name'] = n_selector.css('label::text').extract_first()
            info_map['value'] = v_selector.css('a::text').extract_first()
            information.append(info_map)
        return information

    def product_overview(self, response):
        overview_css = 'section[aria-label="Product Overview"] .collapsable-content ::text'
        return "".join(self.clean(response.css(overview_css).extract()))

    def product_brand(self, response):
        return response.css('img#supplier_logo::attr(alt)').extract_first()

    def product_files(self, response):
        files_title = []
        file_urls = []
        file_selector = response.css('ul#technicalData  a')
        for f_selector in file_selector:
            file_urls.append(f_selector.css('::attr(href)').extract_first())
            files_title.append("".join(self.clean(f_selector.css('::text').extract())))
        return files_title, file_urls

    def product_manufacturer(self, response):
        return response.css('.productDescription .schemaOrg::text').extract_first()

    def product_primary_img_url(self, response):
        return response.css('img#productMainImage::attr(data-full)').extract_first()

    def product_trail(self, response):
        return response.css('.nav nav[role="navigation"] a::text').extract()[1:-1]

    def product_origin_country(self, response):
        origin_xpath = "//dt[contains(text(),'Country')]/following::dd[1]/text()"
        return "".join(self.clean(response.xpath(origin_xpath).extract()))

    def product_tariff_num(self, response):
        tariff_xpath = '//strong[contains(text(), "Tariff")]/following::dd[1]/text()'
        return "".join(self.clean(response.xpath(tariff_xpath).extract()))

    def product_manufacturer_part(self, response):
        return self.clean(response.css('.productDescription dd[itemprop="mpn"] ::text').extract_first())

    def clean(self, to_clean):
        if isinstance(to_clean, str):
            return re.sub('\s+', ' ', to_clean).strip()
        return [re.sub('\s+', ' ', d).strip() for d in to_clean if d.strip()]
