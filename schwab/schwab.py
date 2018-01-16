import scrapy
import re
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from schwab.items import SchwabItem


class SchwabCrawler(CrawlSpider):
    name = "schwab_crawler"
    start_urls = ['https://www.schwab.de/']
    product_api_url = "https://www.schwab.de/index.php?"
    sub_categories_url = "https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true&staticContent=true&cacheID" \
                         "=1514991819"
    item_info_api = "https://www.schwab.de/request/itemservice.php?fnc=getItemInfos"
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="c-productlist c-productlist--4 at-product-list"]'),
             callback='parse_product'),
        Rule(LinkExtractor(restrict_xpaths='.//span[@class="paging__btn"]'), callback='parse')
    )

    def start_requests(self):
        yield scrapy.Request(url=self.sub_categories_url, dont_filter=True, callback=self.parse_start_request)

    def parse_start_request(self, response):
        sub_categories_content = json.loads(response.text)
        for i in sub_categories_content:
            for j in i['sCat']:
                sub_categories_url = j.get("url")
                yield scrapy.Request(url=sub_categories_url, dont_filter=True, callback=self.parse)

    def parse(self, response):
        yield from super().parse(response)

    def title(self, response):
        return response.xpath('.//span[@itemprop="name"]/text()').extract_first().strip()

    def article_no(self, response):
        return response.xpath('.//span[@class="js-artNr at-dv-artNr"]/text()').extract_first().strip()

    def product_details(self, response):
        return self.clean_list(response.xpath('.//div[@itemprop="description"]/text()').extract())

    def description(self, response):
        return self.clean_list(response.xpath('.//ul[@class="l-outsp-bot-5"]//li/text()').extract()) + \
               self.product_details(response)

    def care(self, response):
        care_keys = self.clean_list(response.xpath('.//td[@class="left"]//span/text()').extract())
        care_values = self.clean_list(response.xpath('.//td/text()').extract())
        care_details = {}
        for item in zip(care_keys, care_values):
            care_details[item[0]] = item[1]
        return care_details

    def image_urls(self, response):
        return response.xpath('.//a[@id="magic"]/@href').extract()

    def previous_price(self, response):
        price_xpath = '//span[@class="js-wrong-price pricing__norm--wrong__price"]/text()'
        price = response.xpath(price_xpath).extract_first()
        if price:
            previous_price = price.strip()
            return int(previous_price.replace(',', ''))

    def price(self, response):
        price = response.xpath('.//span[@class="js-detail-price"]/text()').extract_first().strip()
        return int(price.replace(',', ''))

    def colour(self, response):
        colour = response.xpath('.//input[@class="js-current-color-name"]/@value').extract_first()
        if colour:
            return colour.strip()

    def sku_id(self, response):
        return response.xpath('.//input[@name="aid"]/@value').extract_first()

    def currency(self, response):
        return response.xpath('.//meta[@itemprop="priceCurrency"]/@content').extract_first()

    def variant(self, response):
        return response.xpath('.//input[@class="js-current-variant-name"]/@value').extract_first()

    def size_content(self, response):
        return response.xpath('//input[@class="js-current-size-name"]/@value').extract_first()

    def variant_and_size(self, response):
        if self.variant(response):
            if self.size_content(response):
                return self.size_content(response)+"/"+self.variant(response)
            else:
                return self.variant(response)
        else:
            return self.size_content(response)
    
    def article_ids_info(self, response):
        article_text = response.xpath('//script[contains(text(),"articlesString")]/text()').extract_first()
        anid_content = re.findall('\d+\|\d+\|[A-Z0-9|;,]+', article_text)
        return anid_content

    def item_info_request(self, response, item):
        parent_id = self.parent_id(response)
        form_data = {
            'items': self.article_ids_info(response)[0]
        }
        return scrapy.FormRequest(url=self.item_info_api, meta={'parent_id': parent_id, "item": item},
                                  formdata=form_data, callback=self.sku_request)

    def parent_id(self, response):
        return response.xpath('.//input[@name="parentid"]/@value').extract_first()

    def categories_path(self, response):
        return self.clean_list(response.xpath('.//span[@itemprop="name"]/text()').extract())

    def gender(self, response):
        for category in self.categories_path(response):
            if category == "Damen":
                return "Women"
            elif category == "Herren":
                return "Men"
            elif category == "Madchen":
                return "Girl"
            elif category == "Jungen":
                return "Boy"
            elif category == "Kinder":
                return "Kids"
            else:
                return "others"

    def skus(self, response):
        sku = {}
        sku_id = self.sku_id(response)
        sku["previous_price"] = self.previous_price(response)
        sku["price"] = self.price(response)
        sku["color"] = self.colour(response)
        sku["size_content/variant"] = self.variant_and_size(response)
        sku["currency"] = self.currency(response)
        return {sku_id: sku}

    def parse_product(self, response):
        item = SchwabItem()
        item["skus"] = {}
        item["gender"] = self.gender(response)
        item["title"] = self.title(response)
        item["retailer_sku"] = self.article_no(response)
        item["description"] = self.description(response)
        item["care"] = self.care(response)
        item["image_urls"] = self.image_urls(response)
        item["categories"] = self.categories_path(response)
        item["url"] = response.url
        return self.item_info_request(response, item)
    
    def article_ids_content(self, response):
        article_ids_content = json.loads(response.text)
        color_fit_size_content = {}
        color_fit_ids = list(article_ids_content["codes"].keys())
        for color_fit_id in color_fit_ids:
            available_sizes = []
            sizes = article_ids_content["codes"][color_fit_id]
            if isinstance(sizes, dict):
                for size_key, size_value in sizes.items():
                    if size_value != 3:
                        available_sizes.append(size_key)
                color_fit_size_content[color_fit_id] = available_sizes
            else:
                color_fit_size_content[color_fit_id] = '0'
        return color_fit_size_content

    def sku_request(self, response):
        item = response.meta["item"]
        parent_id = response.meta["parent_id"]
        article_ids = []
        for color_fit_content, size_content in self.article_ids_content(response).items():
            color_and_fit_id = re.match('(\d{8}|\d{6})([0-9A-Z]+)', color_fit_content)
            for size in size_content:
                if size == '0':
                    article_ids.append('%s-%s-%s' % (parent_id, color_and_fit_id.group(1), color_and_fit_id.group(2)))
                else:
                    article_ids.append('%s-%s-%s-%s' % (parent_id, color_and_fit_id.group(1), size,
                                                        color_and_fit_id.group(2)))
        multiple_requests = []
        for article_id in article_ids:
            form_data = {
                'cl': "oxwarticledetails",
                'ajaxdetails': 'adsColorChange',
                'anid': article_id,
            }
            request = scrapy.FormRequest(url=self.product_api_url, formdata=form_data, meta={"item": item},
                                         callback=self.parse_sku_request, dont_filter=True)
            multiple_requests.append(request)

        response.meta["sku_request"] = multiple_requests
        response.meta["item"] = item
        return self.request_or_item(response)

    def parse_sku_request(self, response):
        item = response.meta["item"]
        item["skus"].update(self.skus(response))
        return self.request_or_item(response)

    def clean_list(self, my_list):
        final_list = []
        for entry in my_list:
            entry = entry.strip()
            if entry and entry not in final_list:
                final_list.append(entry)
        return final_list

    def request_or_item(self, response):
        sub_requests = response.meta.get("sku_request")
        if sub_requests:
            request = sub_requests.pop()
            request.meta["item"] = response.meta.get("item")
            request.meta["sku_request"] = response.meta.get("sku_request")
            return request
        else:
            return response.meta.get("item")
