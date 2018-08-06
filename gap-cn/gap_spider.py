# -*- coding: utf-8 -*-
import json
from urllib.parse import urljoin, urlsplit

from scrapy.http import FormRequest, HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from gap_parser import GapParser


class GapCrawler(CrawlSpider):
    name = 'gap-cn'
    allowed_domains = ['gap.cn']
    start_urls = ['https://www.gap.cn']

    download_delay = 0.2

    parser = GapParser()
    pagination_url = 'https://www.gap.cn/catalog/category/getCategoryProduct'

    url_query_cleaner = lambda url: urlsplit(url)._replace(query=None).geturl()

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

        cat_id = category_meta_sel.css('::attr(currentcategoryid)').extract_first()
        displayed_prod_css = '::attr(currentcategorydisplaynum{})'.format(cat_id)
        cur_displayed_prod = category_meta_sel.css(displayed_prod_css).extract_first()
        total_products = category_meta_sel.css('::attr(currentcategorytotalnum)').extract_first()

        already_displayed_prod = int(response.meta.get('already_displayed_prod', 0))
        total_displayed_prod = already_displayed_prod + int(cur_displayed_prod)
        if total_displayed_prod < int(total_products):
            all_products_css = '::attr(allproductids{})'.format(cat_id)
            formdata = {
                'allCategoryId': cat_id + ',',
                'lastCategoryId': cat_id,
                'lastCategoryTotalNum': total_products,
                'currentPage': category_meta_sel.css('::attr(currentpage)').extract_first(),
                'haveDisplayAllCategoryId': cat_id + ',',
                'lastCategoryDisplayNum': cur_displayed_prod,
                'productIds': category_meta_sel.css(all_products_css).extract_first()
            }
            return FormRequest(url=self.pagination_url, formdata=formdata,
                               callback=self.parse_page_items,
                               meta={'displayed_num': total_displayed_prod},)

    def parse_page_items(self, response):
        json_res = json.loads(response.text)
        if json_res['status'] == "success":
            ajax_res = HtmlResponse(url=response.url,
                                    body=str.encode(json_res['message']),
                                    request=response.request)
            products_urls = ajax_res.css('.categoryProductItem h5 a::attr(href)').extract()
            for url in products_urls:
                link = GapCrawler.url_query_cleaner(urljoin(response.url, url))
                yield FormRequest(url=link, callback=self.parser.parse_item)

            return self.next_page_req(ajax_res)
