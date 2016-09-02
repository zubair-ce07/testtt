import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sheego_spider.items import SheegoSpiderItem
from operator import add



class SheegoSpider(CrawlSpider):
    name = 'sheego_spider'
    allowed_domains = ['sheego.de']
    start_urls = ['https://www.sheego.de']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//ul[@class="mainnav__ul js-mainnav-ul"]'])),
        Rule(LinkExtractor(restrict_xpaths=['//ul[@class="navigation pl-side-box "]'])),
        Rule(LinkExtractor(restrict_xpaths=['//div[@class="js-product-list-paging paging"]'])),
        Rule(LinkExtractor(restrict_xpaths=['//div[@class="row product__list at-product-list"]']), callback='parse_sheego_item')
    )

    def parse_sheego_item(self, response):
        sheego_item = SheegoSpiderItem()
        sheego_item['gender'] = 'women'
        sheego_item['category'] = ['abc', 'def']
        sheego_item['pid'] = '460721119'
        sheego_item['description'] = self.get_item_description(response)
        sheego_item['brand'] = self.get_item_brand(response)
        sheego_item['image_urls'] = []
        sheego_item['care'] = self.get_item_care(response, sheego_item['description'])
        sheego_item['skus'] = {}
        sheego_item['name'] = self.get_item_name(response)
        sheego_item['url_original'] = response.url
        color_links = [response.urljoin(x) for x in
                        (response.xpath('//div[@class="moreinfo-color colors"]/ul/li/a/@href').extract())]
        return self.find_next_colour(color_links, sheego_item)

    def get_item_brand(self, response):
        return self.normalize_string(response.xpath('//div[@class="brand"]/text()').extract()[0])

    def get_item_name(self, response):
        return self.normalize_string(response.xpath('//span[@itemprop="name"]/text()').extract()[0])

    def get_item_care(self, response, description):
        care = []
        if response.xpath('//div[@class="js-articledetails"]//dl[@class="dl-horizontal articlecare"]/dt').extract():
            care.append(response.xpath(
                '//div[@class="js-articledetails"]//dl[@class="dl-horizontal articlecare"]/dt/text()').extract()[0])
            care.append(response.xpath('//template[@class="js-tooltip-content"]/b/text()').extract()[0])
            if response.xpath('//div[@itemprop="description"]/text()[2]').extract():
                care.append(
                    self.normalize_string(response.xpath('//div[@itemprop="description"]/text()[2]').extract()[0]))
            care.extend([s for s in description if 'Material' in s])
        return care

    def get_item_description(self, response):
        description = response.xpath('//div[@id="moreinfo-highlight"]/ul/li/text()').extract()
        description.append(
            self.normalize_string(response.xpath('//div[@itemprop="description"]/text()[1]').extract()[0]))
        description_types = response.xpath(
            '//div[@class="js-articledetails"]//td[@class="left"]/div/span/text()').extract()
        description_values = response.xpath(
            '//div[@class="js-articledetails"]//td[@class="left"]/following-sibling::td/text()').extract()
        description_types = [x + ' ' for x in description_types]
        description.extend(list(map(add, description_types, description_values)))
        description.append(response.xpath(
            '//div[@class="js-articledetails"]/dl[@class="dl-horizontal articlenumber"]/dt/text()').extract()[0])
        description.append(self.normalize_string(response.xpath(
            '//div[@class="js-articledetails"]/dl[@class="dl-horizontal articlenumber"]/dd/text()').extract()[
                                              0]))
        description = [s for s in description if not 'Material' in s]
        return description

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
            parentid = response.xpath('//input[@name="parentid"]/@value').extract()[0]
            splitted_parentid = parentid.rsplit("-", 1)
            size_data = []
            for size in sizes:
                aid = splitted_parentid[0] + '-' + size.split('/')[0] + '-' + splitted_parentid[1]
                aid = aid[:-1]
                size_data.append(aid)
            formdata = {'aid': aid, 'anid': aid,
                        'parentid': aid}
            return self.find_next_size(response, formdata, size_data, color_links, sheego_item)
        else:
            return sheego_item

    def find_next_size(self, response, formdata, size_data, color_links, sheego_item):
        if size_data:
            aid = size_data.pop()
            formdata['aid'] = aid
            formdata['anid'] = aid
            formdata['parentid'] = aid
            request = scrapy.FormRequest.from_response(response, formdata = formdata, callback=self.parse_size, formnumber=1)
            request.meta['url'] = response
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
        if not (response.xpath('//div[@id="articlenotfound"]').extract() or response.xpath('//div[@class="searchagain"]/h2/text()').extract()):
            price_details = {}
            if response.xpath('//span[@class="lastprice at-lastprice"]/sub').extract():
                price_details['price'] = self.normalize_string(response.xpath('//span[@class="lastprice at-lastprice"]/sub/following-sibling::text()').extract()[
                    0])
                price_details['previous_prices'] = response.xpath('//span[@class="lastprice at-lastprice"]/sub/text()').extract()
            else:
                price_details['previous_prices'] = []
                price_details['price'] = self.normalize_string(response.xpath('//span[@class="lastprice at-lastprice"]/text()').extract()[0])
            price_details['currency'] = 'EUR'
            price_details['colour'] = response.xpath('//span[@class="at-dv-color"]/text()').extract()[0].split(' ')[1]
            price_details['size'] = response.xpath('//span[@class="at-dv-size"]/text()').extract()[0].split(' ')[1]
            sheego_item['skus'][price_details['colour'] + '_' + price_details['size']] = price_details
            return self.find_next_size(url, formdata, size_data, color_links, sheego_item)
        else:
            return self.find_next_size(url, formdata, size_data, color_links, sheego_item)

    def normalize_string(self, input_string):
        return ''.join(input_string.split())