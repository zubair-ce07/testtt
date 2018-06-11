import re
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
from urllib.parse import urlencode
from scrapy.spiders import CrawlSpider, Rule
from scrapylab.items import HonestbeeItemLoader


class WellCome(CrawlSpider):
    name = 'wellcome'
    allowed_domains = ['wellcome.com.hk']
    start_urls = ['https://www.wellcome.com.hk/wd2shop/en/html/index.html']

    listings_xpath = ['//*[contains(@class, "subNavWrapper")]', '//li[contains(@id, "next")]//a']
    products_xpath = ['//*[contains(@class, "brand")]//a']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_xpath), callback='parse'),
        Rule(LinkExtractor(restrict_xpaths=products_xpath), callback='parse_item'),
    )

    # def start_requests(self):
    #     headers = {
    #         'Pragma': 'no-cache',
    #         'Origin': 'https://www.wellcome.com.hk',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    #         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    #         'Content-Type': 'application/x-www-form-urlencoded',
    #         'Accept': 'application/json, text/javascript, */*; q=0.01',
    #         'Cache-Control': 'no-cache',
    #         'X-Requested-With': 'XMLHttpRequest',
    #         'Connection': 'keep-alive',
    #         'Referer': 'https://www.wellcome.com.hk/wd2shop/en/html/shop/detail.html?bj_pdt_id=109640',
    #         "Cookie": "JSESSIONID=5FD955BA064FE6655B0AB80389306CD4; __utmc=114120705; __utmz=114120705.1528714659.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.3.1743623464.1528714659; _gid=GA1.3.886485674.1528714659; __utma=114120705.1743623464.1528714659.1528725331.1528728443.4; __utmt=1; _gat_UA-40785458-4=1; _gali=district_SHOP362; __utmb=114120705.2.10.1528728443"
    #     }
    #
    #     data = [
    #         ('hf_s_id', 'WD11'),
    #         ('hf_srv_id', 'Pv_jpdt_brw'),
    #         ('hs_action_id', 'submit'),
    #         ('hs_rec_per_page', '1'),
    #         ('hs_srch_page_no', '1'),
    #         ('hs_full_detail', 'Y'),
    #         ('hs_pdt_id', '109640'),
    #         # ('hs_pdt_id', self.extract_itemid(response)),
    #         ('hf_locale_id', 'en'),
    #     ]
    #
    #     yield FormRequest('https://www.wellcome.com.hk/wd2/jsp/sys/Sf_render.jsp', headers=headers,
    #                              formdata=data, callback=self.parse_item)

    def extract_itemid(self, response):
        return response.url.re('([\d]{4,})')

    def parse_urls(self, response):
        next_url = response.css('.next::attr(href)').extract_first()
        if next_url:
            request = Request(response.urljoin(next_url), callback=self.parse_urls)
            yield request

        product_urls = response.css('.name a::attr(href)').extract()
        for url in product_urls:
            request = Request(response.urljoin(url), callback=self.parse_item)
            yield request

    def parse_item(self, response):
        loader = HonestbeeItemLoader(response=response)
        raw_json = json.loads(response.text)
        for raw_val in raw_json.get('bvc_pdt'):
            loader.add_value('brand', raw_val.get('bs_brand'))
            loader.add_value('description', raw_val.get('bs_desc'))
            loader.add_value('product_type', raw_val.get('bs_shelf_desc'))
            loader.add_value('barcode', raw_val.get('bs_item_no'))
            loader.add_value('image_urls', response.urljoin(raw_val.get('bs_limg_file')))
            loader.add_value('packaging', raw_val.get('bs_volume'))
            loader.add_value('categories', raw_val.get('bs_dept_desc'))
            loader.add_value('price_per_unit', raw_val.get('bj_psp'))

        loader.add_value('url', response.url)
        yield loader.load_item()
