import scrapy
from turkeyspider2.items import Product
import requests
import urllib

class QuotesSpider(scrapy.Spider):
    name = "product_scraper"
    allowed_domains = ["ozhat-turkiye.com"]
    start_urls = ['http://ozhat-turkiye.com/en/brands-e/']  

    def parse(self, response):
        brands = response.css("div.tabledivinlineblock a.tablelink50::attr(href)").extract()
        i = 0
        for brand in brands:
            next_page = brand
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(url=next_page, callback=self.product_scraper)
        __EVENTTARGET = response.css(
            "span#maincontent_DataPager span.decornonepagerlink ~ a::attr(href)").extract_first()
        if __EVENTTARGET is not None:
            __EVENTTARGET = __EVENTTARGET.split("'")[1]
            __EVENTARGUMENT = ""
            x = response.css("input[value]::attr(value)").extract()
            __VIEWSTATE = x[0]
            __VIEWSTATEGENERATOR = x[1]
            __EVENTVALIDATION = x[2]
            params = {
                '__EVENTTARGET': __EVENTTARGET,
                '__EVENTARGUMENT': __EVENTARGUMENT,
                '__VIEWSTATE': __VIEWSTATE,
                '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                '__EVENTVALIDATION': __EVENTVALIDATION,
                'headers': response.headers
            }
            yield scrapy.FormRequest(url=response.url, callback=self.parse,
                                     method='POST', formdata=params)

    def product_scraper(self, response):
        products = response.css("div.tabledivinlineblock a.tablelink")
        for product in products:
            product_url = product.css("::attr(href)").extract_first()
            product_url = response.urljoin(product_url)
            yield scrapy.Request(url=product_url, callback=self.product_detail)
        __EVENTTARGET = response.css(
            "span#maincontent_DataPager span.decornonepagerlink ~ a::attr(href)").extract_first()
        if __EVENTTARGET is not None:
            __EVENTTARGET = __EVENTTARGET.split("'")[1]
            __EVENTARGUMENT = ""
            x = response.css("input[value]::attr(value)").extract()
            __VIEWSTATE = x[0]
            __VIEWSTATEGENERATOR = x[1]
            __EVENTVALIDATION = x[2]
            params = {
                '__EVENTTARGET': __EVENTTARGET,
                '__EVENTARGUMENT': __EVENTARGUMENT,
                '__VIEWSTATE': __VIEWSTATE,
                '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                '__EVENTVALIDATION': __EVENTVALIDATION,
                'headers': response.headers
            }
            yield scrapy.FormRequest(url=response.url, callback=self.product_scraper,
                                     method='POST', formdata=params)

    def product_detail(self, response):
        item = Product()
        image_urls = list()
        product_img = response.css("div.productimage img::attr(src)").extract_first()
        if 'error' in product_img:
            item['image_urls'] = image_urls
        else:
            product_img = response.urljoin(product_img)
            image_urls.append(product_img)
            item['image_urls'] = image_urls
        product_detail_list = list()
        for product_detail in response.css("div.contallpadding div.productdetail"):
            property_value = product_detail.css("a strong::text").extract_first()
            if property_value is None or property_value == []:
                property_value = product_detail.css("span::text").extract_first()
            product_detail_list.append(property_value)
        len_var = len(product_detail_list)
        if len_var == 3:
            item['manufacturer'] = product_detail_list[0]
            item['product_name'] = product_detail_list[1]
            item['condition'] = product_detail_list[2]

        if len_var == 4:
            item['manufacturer'] = product_detail_list[0]
            item['product_name'] = product_detail_list[1]
            item['technical_specification'] = product_detail_list[2]
            item['condition'] = product_detail_list[3]
        link = ""
        for file in response.css("div.centered ul a.productdownload"):
            file_type = file.css("span::text").extract_first().strip()
            if file_type == 'pdf':
                link = response.urljoin(file.css("::attr(href)").extract_first())
        item['url'] = response.url
        if link != "":
            r = requests.get(link, allow_redirects=True)
            file_name = item['product_name']
            file_name = file_name.replace('/', '_')
            file_name = file_name.replace('-', '_')
            file_name = file_name.replace('.', '_')
            file_name = file_name.replace('*', '')
            file_name = file_name.replace(' ', '')
            file_name = file_name.replace(':', '')
            file_name = file_name + ".pdf"
            file_name = "files/" + file_name
            open(file_name, 'wb').write(r.content)
            item['file_path'] = file_name
        yield item
