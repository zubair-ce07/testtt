import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sheego_spider.items import SheegoSpiderItem



class SheegoSpider(CrawlSpider):
    name = 'sheego_spider'
    allowed_domains = ['sheego.de']
    start_urls = ['https://www.sheego.de']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//ul[@class="mainnav__ul js-mainnav-ul"]', '//ul[@class="navigation pl-side-box "]', '//div[@class="js-product-list-paging paging"]'])),
        Rule(LinkExtractor(restrict_xpaths=['//div[@class="row product__list at-product-list"]']), callback='parse_item')
    )

    def parse_item(self, response):
        item = SheegoSpiderItem()
        item['gender'] = 'women'
        item['category'] = self.item_category(response)
        item['brand'] = self.item_brand(response)
        item['image_urls'] = []
        item['description'], item['care'] = self.item_description_care(response)
        item['skus'] = {}
        item['name'] = self.item_name(response)
        item['url_original'] = response.url
        color_links = [response.urljoin(x) for x in
                        response.xpath('//div[@class="moreinfo-color colors"]/ul/li/a/@href').extract()]
        return self.get_next_colour(color_links, item)

    def get_text(self, response, xpath):
        return ' '.join(response.xpath(xpath).extract())

    def item_category(self, response):
        return response.xpath('//ul[@class="breadcrumb"]/li/a/text()').extract()[1:]

    def item_brand(self, response):
        return self.normalize_string(self.get_text(response, '//div[@class="brand"]/text()')) or\
               self.normalize_string(self.get_text(response, '//div[@class="product-header visible-sm visible-xs"]//div[@class="brand"]/a/text()'))

    def item_name(self, response):
        return self.normalize_string(self.get_text(response, '//div[@class="product-header visible-sm visible-xs"]//span[@itemprop="name"]/text()'))


    def item_description_care(self, response):
        description = response.xpath('//div[@id="moreinfo-highlight"]/ul/li/text()').extract()
        description.append(
            self.normalize_string(self.get_text(response, '//div[@itemprop="description"]//text()')))
        description_selectors = response.xpath('//div[@class="js-articledetails"]//tr')
        for description_selector in description_selectors:
            description.append(self.get_text(description_selector, './/text()'))
        description.append(self.normalize_string(self.get_text(response,
        '//div[@class="js-articledetails"]/dl[@class="dl-horizontal articlenumber"]//text()')))
        care = []
        care_instructions = self.get_text(response,
                                          '//div[@class="js-articledetails"]//dl[@class="dl-horizontal articlecare"]/dt/text()')
        if care_instructions:
            care.append(care_instructions)
            care.append(' '.join(set(response.xpath('//dl[@class="dl-horizontal articlecare"]//template[@class="js-tooltip-content"]/b/text()').extract())))
        item_content = self.get_text(response, '//div[@itemprop="description"]/br/following-sibling::text()')
        if item_content:
                material_content = self.normalize_string(' '.join(item_content))
                # in some cases the item content does not contain material composition
                if '%' in material_content:
                    care.append(material_content)
        care.extend([s for s in description if 'Material' in s])
            # material description needs to be omitted becuase it will be a part of item_care
        return [s for s in description if 'Material' not in s], care

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
        item = response.meta['item']
        color_links = response.meta['color_links']
        sizes = response.xpath(
            '//div[@class="js-sizeSelector cover js-moreinfo-size"]/div/button[not(@disabled = "disabled")]/text()').extract() or response.xpath('//div[@id="variants"]/div/select/option/text()').extract()[1:]
        item['image_urls'].extend(self.item_image_urls(response))
        size_data = []
        if sizes:
            parentid = ' '.join(response.xpath('//input[@name="parentid"]/@value').extract())
            splitted_parentid = parentid.rsplit("-", 1)
            for size in sizes:
                aid = splitted_parentid[0] + '-' + size.split('/')[0] + '-' + splitted_parentid[1]
                aid = aid[:-1]  # the last letter of url (aid) is not needed in form request aid
                size_data.append(aid)
        return self.get_next_size(response, size_data, color_links, item)

    def item_image_urls(self, response):
        return response.xpath('//div[@class="thumbs"]//a/@data-image').extract()

    def get_next_size(self, response, size_data, color_links, item):
        if size_data:
            aid = size_data.pop()
            formdata = {}
            formdata['aid'] = aid
            formdata['anid'] = aid
            formdata['parentid'] = aid
            request = scrapy.FormRequest.from_response(response, formdata = formdata, callback=self.parse_size, formnumber=1)
            request.meta['form_response'] = response
            request.meta['formdata'] = formdata
            request.meta['size_data'] = size_data
            request.meta['color_links'] = color_links
            request.meta['item'] = item
            return request
        else:
            return self.get_next_colour(color_links, item)

    def parse_size(self, response):
        form_response = response.meta['form_response']
        size_data = response.meta['size_data']
        item = response.meta['item']
        color_links = response.meta['color_links']
        if not (response.xpath('//div[@id="articlenotfound"]').extract() or response.xpath('//div[@class="searchagain"]/h2/text()').extract()):
            skus = self.item_sku(response)
            item['skus'][skus['colour'] + '_' + skus['size']] = skus
            return self.get_next_size(form_response, size_data, color_links, item)
        else:
            return self.get_next_size(form_response, size_data, color_links, item)

    def item_sku(self, response):
        skus = {}
        skus['price'], skus['previous_prices'] = self.sku_price(response)
        skus['currency'] = 'EUR'
        skus['colour'] = self.sku_colour(response)
        skus['size'] = self.sku_size(response)
        return skus

    def sku_price(self, response):
        if response.xpath('//span[@class="lastprice at-lastprice"]/sub').extract():
            price = self.normalize_string(
                self.get_text(response, '//span[@class="lastprice at-lastprice"]/sub/following-sibling::text()'))
            previous_prices = [
                self.normalize_string(self.get_text(response, '//span[@class="lastprice at-lastprice"]/sub/text()'))]
        else:
            previous_prices = []
            price = self.normalize_string(
                self.get_text(response, '//span[@class="lastprice at-lastprice"]/text()'))
        return price, previous_prices

    def sku_colour(self, response):
        return ' '.join(response.xpath('//a[@class="color-item active js-ajax "]/@title').extract())

    def sku_size(self, response):
        return response.xpath('//span[@class="at-dv-size"]/text()').extract()[0].split(' ')[1]

    def normalize_string(self, input_string):
        return ''.join(input_string.split())