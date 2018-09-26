# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from HMScrapper.utilities import get, get_first
from HMScrapper.items import HmscrapperItem


class HmSpider(scrapy.Spider):
    name = 'hmspider'
    allowed_domains = ['kw.hm.com/en']
    start_urls = ['https://kw.hm.com/en/']

    def parse(self, response):
        cat_path = "li[class *= 'menu--two__list-item']>div>a::attr(href)"
        categories = response.css(cat_path).extract()
        print(len(categories))
        for category in categories:
            category_url = urljoin(response.url, category)
            print(category_url)
            yield scrapy.Request(url=category_url, callback=self.parse_category, dont_filter=True)

    def parse_category(self, response):
        print("=" * 25)
        print(response.url)
        items_path = "div[class *= 'field__item']>a::attr(href)"
        items = response.css(items_path).extract()
        for item in items:
            item_url = urljoin(response.url, item)
            yield scrapy.Request(url=item_url, callback=self.parse_item, dont_filter=True)
        next_page_path = "li.pager__item>a::attr(href)"
        next_page = response.css(next_page_path).extract_first()
        if next_page:
            next_page_url = urljoin(response.url, next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse_category, dont_filter=True)
        print("=" * 25)

    def parse_item(self, response):
        print(response.url)
        name_path = "div.content__title_wrapper>h1>span::text"
        price_path = "span.price-amount::text"
        item_code_path = "div.content--item-code::text"
        description_path = "div.desc-value::text"
        comp_path = "div.field__content-wrapper div.composition-value>ul>li::text"
        care_info_path = "div.care-instructions-value::text"
        concept_path = "div.concept-value>ul>li::text"

        item = HmscrapperItem()
        item['name'] = get(response, name_path)
        item['composition'] = get(response, comp_path)
        item['price'] = get_first(response, price_path)
        item['concept'] = get_first(response, concept_path)
        item['care_info'] = get_first(response, care_info_path)
        item['description'] = get_first(response, description_path)
        item['item_code'] = get(response, item_code_path)[1].replace("\n", "")
