# -*- coding: utf-8 -*-
import json

from parsel import Selector
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner

from gap_parser import GapParser


class GapCrawler(CrawlSpider):
    name = 'gap-cn'
    allowed_domains = ['gap.cn']
    start_urls = ['https://www.gap.cn']

    download_delay = 0.3

    parser = GapParser()
    pagination_url = 'https://www.gap.cn/catalog/category/getCategoryProduct'

    listing_css = ['#navs', '.treeCenter', '.gapTreeUl']
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_category'),
        Rule(LinkExtractor(restrict_css=('.categoryProductItem'), process_value=url_query_cleaner),
             callback=parser._parse_item),
    )

    def parse_category(self, response):
        categories = response.css('#allCategoryId::attr(value)').extract_first()
        if categories and len(categories[:-1].split(',')) == 1:
            return self.next_page_req(response)

    def next_page_req(self, response):
        category_sel = response.css('.clear1')
        if not category_sel:
            return

        category_id = category_sel.css('::attr(currentcategoryid)').extract_first()
        page_size_css = f'::attr(currentcategorydisplaynum{category_id})'
        page_size = int(category_sel.css(page_size_css).extract_first())
        total_items = int(category_sel.css('::attr(currentcategorytotalnum)').extract_first())
        current_page = int(category_sel.css('::attr(currentpage)').extract_first())

        total_displayed_items = page_size * current_page
        if total_displayed_items < total_items:
            all_products_css = f'::attr(allproductids{category_id})'
            formdata = {
                'allCategoryId': category_id + ',',
                'lastCategoryId': category_id,
                'lastCategoryTotalNum': str(total_items),
                'currentPage': str(current_page),
                'haveDisplayAllCategoryId': category_id + ',',
                'lastCategoryDisplayNum': str(page_size),
                'productIds': category_sel.css(all_products_css).extract_first()
            }
            return FormRequest(url=self.pagination_url, formdata=formdata,
                               callback=self.parse_page_items)

    def parse_page_items(self, response):
        json_response = json.loads(response.text)

        if json_response['status'] != "success":
            return

        ajax_response = Selector(json_response['message'])
        products_urls = ajax_response.css('.categoryProductItem h5 a::attr(href)').extract()

        for url in products_urls:
            link = url_query_cleaner(response.urljoin(url))
            yield FormRequest(url=link, callback=self.parser._parse_item)

        return self.next_page_req(ajax_response)
