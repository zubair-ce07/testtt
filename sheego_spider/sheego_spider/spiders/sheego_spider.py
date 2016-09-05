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
        Rule(LinkExtractor(restrict_xpaths=['//ul[@class="mainnav__ul js-mainnav-ul"]',
                                            '//ul[@class="navigation pl-side-box "]',
                                            '//div[@class="js-product-list-paging paging"]'])),
        Rule(LinkExtractor(restrict_xpaths=['//div[@class="row product__list at-product-list"]']), callback='parse_sheego_item')
    )

    def parse_item(self, response):
        item = SheegoSpiderItem()
        item['gender'] = 'women'
        item['category'] = self.item_category(response)
        item['description'] = self.item_description(response)
        item['brand'] = self.item_brand(response)
        item['image_urls'] = []
        item['care'] = self.item_care(response, item['description'])
        item['skus'] = {}
        item['name'] = self.item_name(response)
        item['url_original'] = response.url
        color_links = [response.urljoin(x) for x in
                        response.xpath('//div[@class="moreinfo-color colors"]/ul/li/a/@href').extract()]
        return self.get_next_colour(color_links, item)

    def item_category(self, response):
        return response.xpath('//ul[@class="breadcrumb"]/li/a/text()').extract()[1:]

    def item_brand(self, response):
        return self.normalize_string(' '.join(response.xpath('//div[@class="brand"]/text()').extract()))\
               or self.normalize_string(' '.join(response.xpath('//div[@class="brand"]/a/text()').extract()))

    def item_name(self, response):
        return self.normalize_string(' '.join(response.xpath('//span[@itemprop="name"]/text()').extract()))

    def item_care(self, response, description):
        care = []
        care_instructions = response.xpath('//div[@class="js-articledetails"]//dl[@class="dl-horizontal articlecare"]/dt/text()').extract()
        if care_instructions:
            care.append(' '.join(care_instructions))
            care.append(' '.join(response.xpath('//template[@class="js-tooltip-content"]/b/text()').extract()))
            item_content = response.xpath('//div[@itemprop="description"]/text()[2]').extract()
            if item_content:
                care.append(
                    self.normalize_string(' '.join(item_content)))
            care.extend([s for s in description if 'Material' in s])
        return care

    def item_description(self, response):
        description = response.xpath('//div[@id="moreinfo-highlight"]/ul/li/text()').extract()
        description.append(
            self.normalize_string(' '.join(response.xpath('//div[@itemprop="description"]/text()[1]').extract())))
        description_types = response.xpath(
            '//div[@class="js-articledetails"]//td[@class="left"]/div/span/text()').extract()
        description_values = response.xpath(
            '//div[@class="js-articledetails"]//td[@class="left"]/following-sibling::td/text()').extract()
        description_types = [x + ' ' for x in description_types]
        description.extend(list(map(add, description_types, description_values)))
        description.append(' '.join(response.xpath(
            '//div[@class="js-articledetails"]/dl[@class="dl-horizontal articlenumber"]/dt/text()').extract()))
        description.append(self.normalize_string(' '.join(response.xpath(
            '//div[@class="js-articledetails"]/dl[@class="dl-horizontal articlenumber"]/dd/text()').extract())))
        description = [s for s in description if not 'Material' in s]
        return description

    def get_next_colour(self, color_links, item):
        if color_links:
            url = color_links.pop()
            request = scrapy.Request(url=url, callback=self.parse_colour, dont_filter=True)
            request.meta['color_links'] = color_links
            request.meta['item'] = item
            return request
        else:
            return item

    def parse_colour(self, response):
        meta = {}
        item = response.meta['item']
        color_links = response.meta['color_links']
        sizes = response.xpath(
            '//div[@class="js-sizeSelector cover js-moreinfo-size"]/div/button[not(@disabled = "disabled")]/text()').extract()
        item['image_urls'].extend(self.item_image_urls(response))
        size_data = []
        aid = []
        formdata = {}
        sizes_availabe = response.xpath('//div[@id="variants"]/div/select/option/text()').extract()[1:]
        if sizes_availabe:
            sizes = sizes_availabe
        if sizes:
            parentid = ' '.join(response.xpath('//input[@name="parentid"]/@value').extract())
            splitted_parentid = parentid.rsplit("-", 1)
            for size in sizes:
                aid = splitted_parentid[0] + '-' + size.split('/')[0] + '-' + splitted_parentid[1]
                aid = aid[:-1]
                size_data.append(aid)
            formdata = {'aid': aid, 'anid': aid,
                        'parentid': aid}
        return self.get_next_size(response, formdata, size_data, color_links, item)

    def item_image_urls(self, response):
        return response.xpath('//div[@class="thumbs"]//a/@data-image').extract()

    def get_next_size(self, response, formdata, size_data, color_links, item):
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
            request.meta['item'] = item
            return request
        else:
            return self.get_next_colour(color_links, item)

    def parse_size(self, response):
        url = response.meta['url']
        formdata = response.meta['formdata']
        size_data = response.meta['size_data']
        item = response.meta['item']
        color_links = response.meta['color_links']
        if not (response.xpath('//div[@id="articlenotfound"]').extract() or response.xpath('//div[@class="searchagain"]/h2/text()').extract()):
            price_details = self.item_skus(response)
            item['skus'][price_details['colour'] + '_' + price_details['size']] = price_details
            return self.get_next_size(url, formdata, size_data, color_links, item)
        else:
            return self.get_next_size(url, formdata, size_data, color_links, item)

    def item_skus(self, response):
        price_details = {}
        if response.xpath('//span[@class="lastprice at-lastprice"]/sub').extract():
            price_details['price'] = self.normalize_string(' '.join(
                response.xpath('//span[@class="lastprice at-lastprice"]/sub/following-sibling::text()').extract()))
            price_details['previous_prices'] = response.xpath(
                '//span[@class="lastprice at-lastprice"]/sub/text()').extract()
        else:
            price_details['previous_prices'] = []
            price_details['price'] = self.normalize_string(
                ' '.join(response.xpath('//span[@class="lastprice at-lastprice"]/text()').extract()))
        price_details['currency'] = 'EUR'
        price_details['colour'] = response.xpath('//span[@class="at-dv-color"]/text()').extract()[0].split(' ')[1]
        price_details['size'] = response.xpath('//span[@class="at-dv-size"]/text()').extract()[0].split(' ')[1]
        return price_details

    def normalize_string(self, input_string):
        return ''.join(input_string.split())