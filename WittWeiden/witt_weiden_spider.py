from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from witt_weiden_spider.items import WittWeidenSpiderItem
import json
import re


class WittWeidenSpider(CrawlSpider):
    name = 'witt_weiden_spider'
    allowed_domains = ['witt-weiden.de']
    start_urls = ['http://www.witt-weiden.de']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths=['//div[@id="content"]//nav',
                             '//div[@id="main-left"]',
                             '//section[@id="content-footer"]'])),
        Rule(LinkExtractor(restrict_xpaths=['//section[@id="content-main"]//article//a'],
                           allow='http://www.witt-weiden.de/\d+'),
             callback='parse_item'))

    def parse_item(self, response):
        item = WittWeidenSpiderItem()
        item['url'] = response.request.url
        item['skus'] = {}
        item['image_urls'] = []
        item['lang'] = 'de'
        item['spider_name'] = WittWeidenSpider.name
        item['retailer'] = 'wittweiden-de'
        item['market'] = 'DE'
        item['brand'] = 'Witt Weiden'
        item['description'] = self.item_description(response)
        item['currency'] = 'EUR'
        item['category'] = self.item_category(response)
        item['name'], item['price'] = self.item_name_price(response)
        meta = {'item': item, 'base_response': response}
        return self.description_request(response, meta)

    def parse_item_description(self, response):
        base_response = response.meta['base_response']
        response.meta['item']['care'] = self.item_care(response)
        return self.buy_box_request(base_response, self.parse_extract_model_variations, response.meta)

    def parse_extract_model_variations(self, response):
        item = response.meta['item']
        source_url = item['url']
        model_variation_links = response.xpath('//div[contains(@id,"model-control-group")]/div//@href').extract()
        if model_variation_links:
            model_variation_links = [source_url + x for x in model_variation_links]
        else:
            model_variation_links = [source_url]
        return self.extract_model_variation_details(model_variation_links, item)

    def parse_model_variation_link(self, response):
        return self.buy_box_request(response, self.parse_color_size_combinations, response.meta)

    def parse_color_size_combinations(self, response):
        base_url = response.meta['item']['url']
        color_links = [base_url + x for x in response.xpath(
            '//div[contains(@id,"color-control-group")]/div//@href').extract()]
        if not color_links:
            article_number = ''.join(response.xpath('//input[contains(@id, "articleNumber")]/@value').extract())
            color_links.append(base_url + '#articleNumber=' + article_number)
        size_links = response.xpath('//div[contains(@id,"size-control-group")]/div//@href').extract()
        sizes = [re.search('(size=\w+)', x).group(1) for x in size_links if x != '#']
        color_size_combination_links = []
        for color_link in color_links:
            for size in sizes:
                color_size_combination_links.append(color_link + '&' + size)
        return self.get_next_color_size_combination(color_size_combination_links, response.meta)

    def parse_item_sku(self, response):
        response.meta['base_response'] = response
        return self.buy_box_request(response, self.parse_buy_box_details, response.meta)

    def parse_buy_box_details(self, response):
        base_response = response.meta['base_response']
        item = response.meta['item']
        sku = self.item_sku(response)
        sku_id = ''.join(response.xpath('//input[contains(@id, "articleNumber")]/@value').extract()) + '_' + sku['size']
        item['skus'][sku_id] = sku
        return self.image_urls_request(base_response, response.meta)

    def parse_image_urls(self, response):
        response.meta['item']['image_urls'].extend(
            [re.sub('\d.jpg', '9.jpg', response.urljoin(x)) for x in response.xpath('//@src').extract()])
        return self.get_next_color_size_combination(response.meta['color_size_combination_links'], response.meta)

    def item_name_price(self, response):
        item_title = ' '.join(response.xpath('//head/title/text()').extract())
        return re.search('(\w+)', item_title).group(1), re.search('(\d+,\d+)', item_title).group(1)

    def item_description(self, response):
        return [' '.join(response.xpath('//div[contains(@id, "description-text")]//text()').extract()).strip()]

    def item_category(self, response):
        category_details = ' '.join(response.xpath('//meta[contains(@name, "WT.z_breadcrumb")]/@content').extract())
        if category_details:
            return category_details.split('>')[1:-1]
        return category_details

    def item_care(self, response):
        care_instructions = [x.strip() for x in
                             response.xpath('//tr[position()=last()-1 or position()=last()]//text()').extract() if
                             x.strip()]
        item_care = []
        while care_instructions:
            care = care_instructions.pop(0)
            if 'Pflege:' == care or 'Material:' == care:
                item_care.append(care)
                item_care.append(care_instructions.pop(0))
        return item_care

    def create_query_string(self, response):
        query_string = ''
        if '#' in response.request.url:
            query_string = re.search('#(.+)', response.request.url).group(1)
        product_details = json.loads(
            response.xpath('//section[contains(@id,"product-detail")]/@data-product').extract()[0])
        for product_detail in product_details:
            query_string = query_string + '&' + product_detail + '=' + product_details[product_detail]
        return query_string

    def extract_model_variation_details(self, model_variation_links, item):
        if not model_variation_links:
            item['image_urls'] = list(set(item['image_urls']))
            return item
        model_variation_link = model_variation_links.pop(0)
        return Request(url=model_variation_link, callback=self.parse_model_variation_link,
                       meta={'model_variation_links': model_variation_links, 'item': item}, dont_filter=True)

    def get_next_color_size_combination(self, color_size_combination_links, meta):
        if not color_size_combination_links:
            return self.extract_model_variation_details(meta['model_variation_links'], meta['item'])
        color_size_combination_link = color_size_combination_links.pop(0)
        meta['color_size_combination_links'] = color_size_combination_links
        return Request(url=color_size_combination_link, callback=self.parse_item_sku,
                       meta=meta, dont_filter=True)

    def item_sku(self, response):
        sku = {}
        sku['price'] = self.sku_price(response)
        sku['currency'] = 'EUR'
        sku['color'] = self.sku_color(response)
        sku['size'] = self.sku_size(response)
        previous_price = self.sku_previous_price(response)
        if previous_price:
            sku['previous_price'] = previous_price
        return sku

    def sku_price(self, response):
        return ''.join(response.xpath('//p[contains(@class, "price")]/strong//text()').extract())

    def sku_color(self, response):
        return ''.join(response.xpath('//input[contains(@id, "color")]/@value').extract())

    def sku_size(self, response):
        return ''.join(response.xpath('//input[contains(@id, "size")]/@value').extract())

    def sku_previous_price(self, response):
        return ''.join(response.xpath('//p[contains(@class, "price")]/strike//text()').extract())

    def image_urls_request(self, response, meta):
        query_string = self.create_query_string(response)
        return Request(url='http://www.witt-weiden.de/ajax/product-detail/inspection-images.html?' + query_string,
                       callback=self.parse_image_urls,
                       headers={'X-Requested-With': 'XMLHttpRequest'},
                       meta=meta,
                       dont_filter=True)

    def buy_box_request(self, response, callback, meta):
        query_string = self.create_query_string(response)
        return Request(url='http://www.witt-weiden.de/ajax/product-detail/buy-box.html?' + query_string,
                       callback=callback,
                       headers={'X-Requested-With': 'XMLHttpRequest'},
                       meta=meta,
                       dont_filter=True)

    def description_request(self, response, meta):
        query_string = self.create_query_string(response)
        return Request(url='http://www.witt-weiden.de/ajax/product-detail/description-table.html?' + query_string,
                       callback=self.parse_item_description,
                       headers={'X-Requested-With': 'XMLHttpRequest'},
                       meta=meta,
                       dont_filter=True)
