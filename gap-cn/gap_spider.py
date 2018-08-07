# -*- coding: utf-8 -*-
import json
from urllib.parse import urljoin, urlsplit

from scrapy.http import FormRequest, HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner

from gap_parser import GapParser


class GapCrawler(CrawlSpider):
    name = 'gap-cn'
    allowed_domains = ['gap.cn']
    start_urls = ['https://www.gap.cn']

    download_delay = 0.2

    parser = GapParser()
    pagination_url = 'https://www.gap.cn/catalog/category/getCategoryProduct'

    listing_css = ['#navs', '.treeCenter', '.gapTreeUl']
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_category'),
        Rule(LinkExtractor(restrict_css=('.categoryProductItem'), process_value=url_query_cleaner),
             callback=parser.parse_item),
    )

    def parse_category(self, response):
        categories = response.css('#allCategoryId::attr(value)').extract_first()
        if categories and len(categories[:-1].split(',')) == 1:
            return self.next_page_req(response)

    def next_page_req(self, response):
        category_meta_sel = response.css('.clear1')
        if not category_meta_sel:
            return

        category_id = category_meta_sel.css('::attr(currentcategoryid)').extract_first()
        current_displayed_items_css = f'::attr(currentcategorydisplaynum{category_id})'
        current_displayed_items = category_meta_sel.css(current_displayed_items_css).extract_first()
        total_items = category_meta_sel.css('::attr(currentcategorytotalnum)').extract_first()

        already_displayed_items = int(response.meta.get('total_displayed_items', 0))
        total_displayed_items = already_displayed_items + int(current_displayed_items)
        if total_displayed_items < int(total_items):
            all_products_css = f'::attr(allproductids{category_id})'
            formdata = {
                'allCategoryId': category_id + ',',
                'lastCategoryId': category_id,
                'lastCategoryTotalNum': total_items,
                'currentPage': category_meta_sel.css('::attr(currentpage)').extract_first(),
                'haveDisplayAllCategoryId': category_id + ',',
                'lastCategoryDisplayNum': current_displayed_items,
                'productIds': category_meta_sel.css(all_products_css).extract_first()
            }
            return FormRequest(url=self.pagination_url, formdata=formdata,
                               callback=self.parse_page_items,
                               meta={'total_displayed_items': total_displayed_items},)

    def parse_page_items(self, response):
        json_res = json.loads(response.text)
        if json_res['status'] == "success":
            ajax_res = HtmlResponse(url=response.url,
                                    body=str.encode(json_res['message']),
                                    request=response.request)
            products_urls = ajax_res.css('.categoryProductItem h5 a::attr(href)').extract()
            for url in products_urls:
                link = url_query_cleaner(urljoin(response.url, url))
                yield FormRequest(url=link, callback=self.parser.parse_item)

            return self.next_page_req(ajax_res)
