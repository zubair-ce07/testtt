import re
import scrapy
from KITH.items import KithItem


class KITHY(scrapy.Spider):
    name = "scrapy_KITH"
    allowed_domains = ["kith.com"]
    start_urls = ['https://kith.com/']

    def parse_products(self, response):

        for href in response.xpath('//a[contains(@class,"product-card-info")]/@href'):
            url = "https://kith.com" + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

        next_page_url = response.xpath('//span[contains(@class,"next")]/a/@href').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse(self, response):

        href_list = response.xpath('//ul[contains(@class, "ksplash-mega-list")]/li/a/@href').extract()
        for href in href_list:
            yield scrapy.Request(href, callback=self.parse_products)

    def parse_dir_contents(self, response):
        item = KithItem()
        description_list = []

        i_iterator = 1
        description_xpath = '//div[contains(@class,"product-single-details-rte rte mb0")]/p[{}]/text()'
        while response.xpath(description_xpath.format(i_iterator)).extract_first() != u'\xa0' and \
                response.xpath(description_xpath.format(i_iterator)).extract_first() is not None and \
                'Style' not in response.xpath(description_xpath.format(i_iterator)).extract_first():
            description_list.append(response.xpath(description_xpath.format(i_iterator)).extract_first())
            i_iterator = i_iterator + 1

        item['description'] = description_list + response.xpath(
            '//div[contains(@class, "product-single-details-rte rte mb0")]/ul/li/text()').extract()

        j_iterator = 1
        style_xpath = '//div[contains(@class, "product-single-details-rte rte mb0")]/p[{}]/text()'
        while True:
            if response.xpath(style_xpath.format(j_iterator)).extract_first() != u'\xa0':
                sub_string_style = re.search('Style: (.+?)$',
                                             response.xpath(style_xpath.format(j_iterator)).extract_first())
                if sub_string_style:
                    item['product_ID'] = sub_string_style.group(1)
                    break
            j_iterator = j_iterator + 1

        k_iterator = 1
        material_xpath = '//div[contains(@class,"product-single-details-rte rte mb0")]/p[{}]/text()'
        while True:
            if response.xpath(material_xpath.format(k_iterator)).extract_first() != u'\xa0':
                sub_string_mat = re.search('Material: (.+?)$',
                                           response.xpath(material_xpath.format(k_iterator)).extract_first())
                if sub_string_mat:
                    item['material'] = sub_string_mat.group(1)
                    break
            k_iterator = k_iterator + 1

        item['name'] = response.xpath('//h1[contains(@class,"product-header-title")]/text()').extract_first().strip()
        item['color'] = response.xpath('//span[contains(@class,'
                                       '"product-header-title -variant")]/text()').extract_first().strip()
        item['price'] = (response.xpath('//span[@id="ProductPrice"]/text()').extract_first()).strip()
        item['img_urls'] = response.xpath('//img[contains(@class, '
                                          '"js-super-slider-photo-img super-slider-photo-img")]/@src').extract()
        price = response.xpath('//span[@id="ProductPrice"]/text()').extract_first().strip()
        item['currency'] = price[:1]
        item['sizes'] = response.xpath('//div[contains(@class, '
                                       '"product-single-form-item -dropdown -full")]'
                                       '/select/option/text()').extract()
        item['url'] = response.url

        yield item



