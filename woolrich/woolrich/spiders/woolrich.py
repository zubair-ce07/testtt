import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import w3lib.url
from urllib.parse import parse_qsl
from woolrich.items import WoolRichItem


class WoolRich(CrawlSpider):
    name = "wool_rich_crawler"
    allowed_domains = ["woolrich.com"]
    start_urls = ["http://www.woolrich.com/"]
    product_api_url = "http://www.woolrich.com/woolrich/prod/fragments/productDetails.jsp"
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="menu-bar"]', tags="a", attrs="href"),),
        Rule(LinkExtractor(restrict_xpaths='.//div[@class="clear addMore"]', tags='div', attrs='next_page'),),
        Rule(LinkExtractor(restrict_xpaths='.//div[@class="hover_img "]', tags='a', attrs='href'),
             callback='parse_product')
    )

    def image_urls(self, response):
        images_url = []
        images = response.xpath('.//ul[@class="colorlist"]//a//img/@src').extract()
        for image in images:
            url = image.replace('swatch', 'large')
            url = w3lib.url.url_query_cleaner(url, ['version'], remove=True)
            images_url.append(url)
        return images_url

    def product_title(self, response):
        return response.xpath('.//div[@class="pdp_title"]//h1/text()').extract_first()

    def brand_name(self, response):
        return "Woolrich"

    def retailer_sku(self, response):
        return response.xpath('.//div[@class="pdp "]/@productid').extract_first()

    def product_description(self, response):
        description = response.xpath('.//span[@itemprop="description"]/text()').extract()
        if description:
            return description
        else:
            description = response.xpath('.//span[@itemprop="description"]/text()').extract()
            return description

    def product_care(self, response):
        return response.xpath('.//div[@class="text"]//li/text()').extract()

    def product_category(self, response):
        return response.xpath('.//div[@class="wrap breadcrumb"]//a/text()').extract()[1:]

    def product_currency(self, response):
        return response.xpath('.//span[@itemprop="priceCurrency"]/text()').extract_first()

    def product_url(self, response):
        return response.xpath('.//link[@rel="canonical"]/@href').extract_first()

    def sku_color(self, response):
        color = response.xpath('.//span[@class="colorName"]/text()').extract_first()
        return color.replace(u"\xa0", u"")

    def sku_price(self, response):
        price = response.xpath('.//span[@itemprop="price"]/@content').extract_first()
        return price.strip()

    def sku_size(self, response):
        return response.css('.sizelist .selected ::text').extract_first()

    def sku_currency(self, response):
        return response.xpath('.//span[@itemprop="priceCurrency"]/text()').extract_first()

    def sku_old_price(self, response):
        price = response.xpath('.//span[@class="price_reg strikethrough"]/text()').extract_first()
        if price:
            old_price = price.strip()
            return old_price.replace(u'\xa0', u'')

    def sku_id(self, response):
        return response.css('.sizelist .selected ::attr("id")').extract_first()

    def fit_sku_id(self, response):
        return response.css('.dimensionslist .selected ::attr("id")').extract_first()

    def sku_fitting(self, response):
        fitting = response.css('.dimensionslist .selected ::text').extract_first()
        return fitting.strip()

    def size_skus(self, response):
        skus = {}
        sku_id = self.sku_id(response)
        skus[sku_id] = {}
        skus[sku_id]["size"] = self.sku_size(response)
        skus[sku_id]["color"] = self.sku_color(response)
        skus[sku_id]["price"] = self.sku_price(response)
        skus[sku_id]["currency"] = self.sku_currency(response)
        skus[sku_id]["old_price"] = self.sku_old_price(response)
        return skus

    def fit_skus(self, response):
        skus = {}
        fit_sku_id = self.fit_sku_id(response)
        size = self.sku_size(response)
        skus[fit_sku_id] = {}
        skus[fit_sku_id]["color"] = self.sku_color(response)
        skus[fit_sku_id]["price"] = self.sku_price(response)
        skus[fit_sku_id]["currency"] = self.sku_currency(response)
        skus[fit_sku_id]["old_price"] = self.sku_old_price(response)
        skus[fit_sku_id]["size"] = size+"/"+self.sku_fitting(response)
        return skus

    def parse_product(self, response):
        item = WoolRichItem()
        item["skus"] = {}
        item["url_original"] = response.url
        item["url"] = self.product_url(response)
        item["image_urls"] = self.image_urls(response)
        item["title"] = self.product_title(response)
        item["retailer_sku"] = self.retailer_sku(response)
        item["brand_name"] = self.brand_name(response)
        item["description"] = self.product_description(response)
        item["care"] = self.product_care(response)
        item["category"] = self.product_category(response)
        item["currency"] = self.product_currency(response)
        item["requests"] = self.color_requests(response, item)
        return self.request_or_item(item)

    def color_requests(self, response, item):
        color_requests = []
        product_id = response.xpath('.//span[@itemprop="productID"]/text()').extract_first()
        color_ids = response.xpath('.//ul[@class="colorlist"]//a//img/@colorid').extract()
        color_names = response.xpath('.//ul[@class="colorlist"]//a/@title').extract()
        for c_id, name in zip(color_ids, color_names):
            form_data = {
                'productId': product_id,
                'colorId': c_id,
                'colorDisplayName': name,
            }
            request = scrapy.FormRequest(url=self.product_api_url, formdata=form_data, meta={"item": item},
                                         dont_filter=True, callback=self.parse_color)
            color_requests.append(request)
        return color_requests

    def parse_color(self, response):
        size_requests = []
        item = response.meta["item"]
        form_data = dict(parse_qsl(response.request.body.decode()))
        sizes = response.xpath('.//ul[@class="sizelist"]//a[@stocklevel!="0"]/@title').extract()
        sku_ids = response.xpath('.//ul[@class="sizelist"]//a[@stocklevel!="0"]/@id').extract()
        for size, s_id in zip(sizes, sku_ids):
            form_data["selectedSize"] = size
            form_data["skuId"] = s_id
            request = scrapy.FormRequest(url=self.product_api_url, formdata=form_data,
                                         meta={"item": item}, dont_filter=True, callback=self.parse_size)
            size_requests.append(request)
        item["requests"] += size_requests
        return self.request_or_item(item)

    def fit_requests(self, response, item, form_data):
        fit_requests = []
        is_fit_exist = response.css('.dimensionslist').extract()
        if is_fit_exist:
            available_fits = response.xpath('.//ul[@class="dimensionslist"]//a[@stocklevel!="0"]/@title').extract()
            sku_ids = response.xpath('.//ul[@class="dimensionslist"]//a[@stocklevel!="0"]/@id').extract()
            for fit, s_id in zip(available_fits, sku_ids):
                form_data["skuId"] = s_id
                form_data["selectedDimension"] = fit
                request = scrapy.FormRequest(url=self.product_api_url, formdata=form_data, meta={"item": item},
                                             dont_filter=True, callback=self.parse_fitting)
                fit_requests.append(request)
        return fit_requests

    def parse_size(self, response):
        form_data = dict(parse_qsl(response.request.body.decode()))
        item = response.meta["item"]
        if self.fit_requests(response, item, form_data):
            item["requests"] += self.fit_requests(response, item, form_data)
            return self.request_or_item(item)
        else:
            item["skus"].update(self.size_skus(response))
            return self.request_or_item(item)

    def parse_fitting(self, response):
        item = response.meta["item"]
        item["skus"].update(self.fit_skus(response))
        return self.request_or_item(item)

    def request_or_item(self, item):
        if item["requests"]:
            return item["requests"].pop()
        else:
            del item['requests']
            return item