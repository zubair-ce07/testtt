"""
This module crawls pages and gets data.
"""
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
import requests


class Lindex(CrawlSpider):
    """This class crawls lindex pages"""
    name = 'lindex'
    allowed_domains = ['lindex.com']
    start_urls = ['https://www.lindex.com/uk/']
    rules = [
        Rule(LinkExtractor(
            allow=['/women/', '/kids/', '/beauty/', '/lingerie/', '/sale/'], restrict_css=['li'],),
             callback='parse_category'),
    ]

    def parse_category(self, response):
        """This method crawls item detail information."""
        nodeid = response.css('body::attr(data-page-id)').extract_first()
        pages = response.css(
            'div.gridPages::attr(data-page-count)').extract_first()
        print("PAGES: ", pages)
        for page_num in range(1, int(pages)):
            yield scrapy.FormRequest(
                url='https://www.lindex.com/uk/SiteV3/Category/GetProductGridPage',
                headers={
                    'X-requested-with': 'XMLHttpRequest',
                    'Path': '/uk/SiteV3/Category/GetProductGridPage',
                    'Accept': 'text/html, */*; q=0.01',
                    'Cache-Control': 'no-cache',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                formdata={
                    'nodeId': nodeid,
                    'pageIndex': str(page_num),
                },
                callback=self.parse_product)

    def parse_product(self, response):
        """This method crawls item information."""
        product_info = response.css(".info>a::attr(href)").extract()
        for detail_url in product_info:
            yield scrapy.Request(url=response.urljoin(detail_url),
                                 callback=self.parse_product_detail)

    def parse_product_detail(self, response):
        """This method crawls item detail information."""
        title = response.css('.info>h1>span::text').extract_first()
        desc = response.css('.description>p::text').extract_first()
        product_facts = response.css('.description>ul>li::text').extract()
        product_id = response.css('.product_id::text').extract()
        color_id = response.css(
            '.info_wrapper>ul.colors>li>a::attr(data-colorid)').extract()
        product_info = {
            'title': title.strip(),
            'description': desc.strip(),
            'product_facts': product_facts,
            'product_id': product_id[1].strip(),
        }
        size_color_details = []
        for data in color_id:
            url = 'https://www.lindex.com/WebServices/ProductService.asmx/GetProductData'
            payload = {
                'colorId': str(data),
                'primaryImageType': '1',
                'productIdentifier': str(product_id[1].strip()),
            }
            headers = {
                'X-requested-with': 'XMLHttpRequest',
                'Path': '/WebServices/ProductService.asmx/GetProductData',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/json; charset=UTF-8'}
            color_data = requests.post(
                url=url, json=payload, headers=headers)
            jsonresponse = color_data.json()
            color = jsonresponse['d']['Color']
            price = jsonresponse['d']['Price']
            sizes = jsonresponse['d']['SizeInfo']
            sku_id = jsonresponse['d']['SKUID']
            size_data = []
            color_and_price = {
                'color': color,
                'price': price,
            }
            for value in range(1, len(sizes)):
                size_data.append(sizes[value]['Text'])

            size_color_data = {
                sku_id: color_and_price,
                'sizes': size_data
            }
            size_color_details.append(size_color_data)
        product_details = {
            'product_info': product_info,
            'size_color_details': size_color_details,
        }
        yield product_details
