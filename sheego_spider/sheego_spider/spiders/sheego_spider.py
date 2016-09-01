import scrapy
from scrapy.spiders import Spider
from sheego_spider.items import SheegoSpiderItem
from operator import add
import re
from scrapy import FormRequest


class SheegoSpider(Spider):
    name = 'sheego_spider'
    allowed_domains = ['sheego.de']
    start_urls = ['https://www.sheego.de']

    def parse(self, response):
        all_category_links = [response.urljoin(x) for x in (response.xpath('//ul[@class="mainnav__ul js-mainnav-ul"]/li/a/@href').extract())]
        all_category_links = all_category_links[1:6]
        del all_category_links[3]
        category_names = response.xpath('//ul[@class="mainnav__ul js-mainnav-ul"]/li/a/div/following-sibling::text()').extract()
        category_names = category_names[:-1]
        sub_tree_ids = ["categorysubtree_3b840f10ff4013fb5c8a8b661fa84813","categorysubtree_3b840f10ff4013fb5c8a8b661f8e584b",
                        "categorysubtree_3b840f10ff4013fb5c8a8b661f522c7d","categorysubtree_4813665079db503bf3f47b6accc8b6e7"]
        for category_link in all_category_links:
            request = scrapy.Request(url=category_link, callback=self.parse_category)
            request.meta['category_name'] = category_names.pop()
            request.meta['subtree_id'] = sub_tree_ids.pop()
            yield request

    def parse_category(self, response):
         category_name = response.meta['category_name']
         subtree_id = response.meta['subtree_id']
         sub_category_links = [response.urljoin(x) for x in (response.xpath('//ul[@id="'+subtree_id+'"]/li/a/@href').extract())]
         sub_category_names = response.xpath('//ul[@id="'+subtree_id+'"]/li/a/strong/text()').extract()
         for sub_category_link in sub_category_links:
             request = scrapy.Request(url=sub_category_link, callback=self.parse_sub_category)
             request.meta['category_name'] = category_name
             request.meta['sub_category_name'] = sub_category_names.pop()
             yield request

    def parse_sub_category(self, response):
        category_name = response.meta['category_name']
        sub_category_name = response.meta['sub_category_name']
        page_links = [response.urljoin(x) for x in (response.xpath('//div[@class="js-product-list-paging paging"]/div/a/@href').extract())]
        for each_page in page_links:
            request = scrapy.Request(url=each_page, callback=self.parse_product)
            request.meta['category_name'] = category_name
            request.meta['sub_category_name'] = sub_category_name
            yield request

    def parse_product(self, response):
        category_name = response.meta['category_name']
        sub_category_name = response.meta['sub_category_name']
        products = set([response.urljoin(x) for x in
                    (response.xpath('//div[@class="js-productList"]/div/div/div/div/a/@href').extract())])
        for product in products:
            sheego_item = SheegoSpiderItem()
            sheego_item['gender'] = 'women'
            sheego_item['category'] = [category_name, sub_category_name]
            sheego_item['pid'] = '460721119'
            request = scrapy.Request(url=product, callback=self.parse_sheego_item, dont_filter=True)
            request.meta['sheego_item'] = sheego_item
            return request

    def parse_sheego_item(self, response):
        sheego_item = response.meta['sheego_item']
        sheego_item['description'] = []
        sheego_item['description'].extend(response.xpath('//div[@id="moreinfo-highlight"]/ul/li/text()').extract())
        sheego_item['description'].append(
            response.xpath('//div[@itemprop="description"]/text()[1]').extract()[0].strip())
        description_types = response.xpath(
            '//div[@class="js-articledetails"]//td[@class="left"]/div/span/text()').extract()
        description_values = response.xpath(
            '//div[@class="js-articledetails"]//td[@class="left"]/following-sibling::td/text()').extract()
        description_types = [x + ' ' for x in description_types]
        sheego_item['description'].extend(list(map(add, description_types, description_values)))
        sheego_item['description'].append(response.xpath(
            '//div[@class="js-articledetails"]/dl[@class="dl-horizontal articlenumber"]/dt/text()').extract()[0])
        sheego_item['description'].append(response.xpath(
            '//div[@class="js-articledetails"]/dl[@class="dl-horizontal articlenumber"]/dd/text()').extract()[
                                              0].strip())
        sheego_item['brand'] = response.xpath('//div[@class="brand"]/text()').extract()[0].strip()
        sheego_item['image_urls'] = []
        sheego_item['care'] = []
        sheego_item['skus'] = dict()
        if int(response.xpath('boolean(//div[@class="js-articledetails"]//dl[@class="dl-horizontal articlecare"]/dt)').extract()[0]):
            sheego_item['care'].append(response.xpath(
                '//div[@class="js-articledetails"]//dl[@class="dl-horizontal articlecare"]/dt/text()').extract()[0])
            sheego_item['care'].append(response.xpath('//template[@class="js-tooltip-content"]/b/text()').extract()[0])
            if int(response.xpath('boolean(//div[@itemprop="description"]/text()[2])').extract()[0]):
                sheego_item['care'].append(response.xpath('//div[@itemprop="description"]/text()[2]').extract()[0].strip())
            sheego_item['care'].extend([s for s in sheego_item['description'] if 'Material' in s])
        sheego_item['description'] = [s for s in sheego_item['description'] if not 'Material' in s]
        sheego_item['name'] = response.xpath('//span[@itemprop="name"]/text()').extract()[0].strip()
        sheego_item['url_original'] = response.url
        color_links = [response.urljoin(x) for x in
                        (response.xpath('//div[@class="moreinfo-color colors"]/ul/li/a/@href').extract())]
        return self.find_next_colour(color_links, sheego_item, )

    def find_next_colour(self, color_links, sheego_item):
        if color_links:
            url = color_links.pop()
            request = scrapy.Request(url=url, callback=self.parse_colour, dont_filter=True)
            request.meta['color_links'] = color_links
            request.meta['sheego_item'] = sheego_item
            return request
        else:
            return sheego_item

    def parse_colour(self, response):
        sheego_item = response.meta['sheego_item']
        color_links = response.meta['color_links']
        sizes = response.xpath(
            '//div[@class="js-sizeSelector cover js-moreinfo-size"]/div/button[not(@disabled = "disabled")]/text()').extract()
        sheego_item['image_urls'].extend(response.xpath('//div[@class="thumbs"]//a/@data-image').extract())
        if response.xpath('//div[@id="variants"]/div/select/option/text()').extract()[1:]:
            sizes = response.xpath('//div[@id="variants"]/div/select/option/text()').extract()[1:]
        if sizes:
            #stoken = response.xpath('//input[@name="stoken"]/@value').extract()[0]
            lang = response.xpath('//input[@name="lang"]/@value').extract()[0]
            actcontrol = response.xpath('//input[@name="actcontrol"]/@value').extract()[0]
            currentImage = response.xpath('//input[@name="currentImage"]/@value').extract()[0]
            artNr = response.xpath('//input[@name="artNr"]/@value').extract()[0]
            artName = response.xpath('//input[@name="artName"]/@value').extract()[0]
            cl = response.xpath('//input[@name="actcontrol"]/@value').extract()[0]
            parentid = response.xpath('//input[@name="parentid"]/@value').extract()[0]
            selectFirstDeliverableProduct = \
                response.xpath('//input[@name="selectFirstDeliverableProduct"]/@value').extract()[0]
            econdapath = re.search('sEcondaPath = \'(.+?(?=\'))',
                                   response.xpath('//script[@type="text/javascript"]/text()').extract()[3]).group(1)
            am = '1'
            ajaxdetails = 'ajaxdetailsPage'
            index_of_size_insertion = parentid.rfind("-")
            size_data = []
            for size in sizes:
                aid = parentid[:index_of_size_insertion] + '-' + size.split('/')[0] + '-' + parentid[index_of_size_insertion+1:]
                aid = aid[:-1]
                size_data.append(aid)
            formdata = {'lang': lang, 'actcontrol': actcontrol,
                        'currentImage': currentImage, 'artNr': artNr, 'artName': artName,
                        'cl': cl, 'aid': aid, 'anid': aid,
                        'parentid': aid,
                        'selectFirstDeliverableProduct': selectFirstDeliverableProduct,
                        'econdapath': econdapath,
                        'am': am, 'ajaxdetails': ajaxdetails}
            return self.find_next_size(response.url, formdata, size_data, color_links, sheego_item)
        else:
            sheego_item['skus'] = ['Not Available']
            return sheego_item

    def find_next_size(self, url, formdata, size_data, color_links, sheego_item):
        if size_data:
            aid = size_data.pop()
            formdata['aid'] = aid
            formdata['anid'] = aid
            formdata['parentid'] = aid
            request = FormRequest(url=url, formdata = formdata, callback=self.parse_size)
            request.meta['url'] = url
            request.meta['formdata'] = formdata
            request.meta['size_data'] = size_data
            request.meta['color_links'] = color_links
            request.meta['sheego_item'] = sheego_item
            return request
        else:
            return self.find_next_colour(color_links, sheego_item)


    def parse_size(self, response):
        url = response.meta['url']
        formdata = response.meta['formdata']
        size_data = response.meta['size_data']
        sheego_item = response.meta['sheego_item']
        color_links = response.meta['color_links']
        if not int(response.xpath('boolean(//div[@id="articlenotfound"])').extract()[0]):
            price_details = {}
            if int(response.xpath('boolean(//span[@class="lastprice at-lastprice"]/sub)').extract()[0]):
                price_details['price'] = response.xpath('//span[@class="lastprice at-lastprice"]/sub/following-sibling::text()').extract()[
                    0].strip()
                price_details['previous_prices'] = response.xpath('//span[@class="lastprice at-lastprice"]/sub/text()').extract()
            else:
                price_details['previous_prices'] = []
                price_details['price'] = response.xpath('//span[@class="lastprice at-lastprice"]/text()').extract()[0]
            price_details['currency'] = 'EUR'
            price_details['colour'] = response.xpath('//span[@class="at-dv-color"]/text()').extract()[0].split(' ')[1]
            price_details['size'] = response.xpath('//span[@class="at-dv-size"]/text()').extract()[0].split(' ')[1]
            sheego_item['skus'][price_details['colour'] + '_' + price_details['size']] = price_details
            return self.find_next_size(url, formdata, size_data, color_links, sheego_item)
        else:
            return self.find_next_size(url, formdata, size_data, color_links, sheego_item)



