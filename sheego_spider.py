import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlencode
from scrapy import Request

from ..items import SheegoItem


class UrbanLocker(CrawlSpider):
    name = 'sheego'
    allowed_domains = ['sheego.de']
    start_urls = ['https://www.sheego.de/']
    listings_xpath = ['//section[contains(@class, "cj-mainnav")]', '//span[contains(@class, "paging__btn")]//a']
    products_xpath = ['//a[contains(@class, "product__top")]']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_xpath), callback='parse'),
        Rule(LinkExtractor(restrict_xpaths=products_xpath), callback='parse_item'),
    )

    currency_map = {
        "€": "EUR"
    }

    def parse_item(self, response):
        item = SheegoItem()
        item['url'] = response.url

        item['retailer_sku'] = self.product_retailer_sku(response)
        item['currency'] = self.product_currency(response)
        item['category'] = self.product_category(response)
        item['name'] = self.product_name(response)
        item['brand'] = self.product_brand(response)
        item['image_urls'] = self.image_urls(response)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['skus'] = []

        return self.call_requests(self.sku_url_requests(response), item)

    def call_requests(self, requests, item):
        if requests:
            request = requests.pop(0)
            request.meta['item'] = item
            request.meta['requests'] = requests
            yield request
        else:
            yield item

    def parse_skus(self, response):
        item = response.meta['item']
        item['skus'].append(self.sku(response))
        requests = response.meta['requests']
        return self.call_requests(requests, item)

    def sku(self, response):
        color = self.product_colour(response)
        size = self.product_size(response)
        price, previous_prices = self.product_pricing(response)
        raw_size = self.product_dropdown_size(response)

        out_of_stock = self.product_outofstock(response)
        sku = {
            'price': price,
            'previous_price': previous_prices,
            'size': size,
            'color': color,
            'sku_id': "{}_{}".format(color, size)
        }
        if out_of_stock:
            sku['out_of_stock'] = out_of_stock
        if raw_size:
            sku['sku_id'] = "{}_{}/{}".format(color, raw_size.strip(), size)
            sku['size'] = "{}/{}".format(raw_size.strip(), size)
        return sku

    def sku_url_requests(self, response):
        color_varsel_ids = self.url_color_varselids(response)
        size_varsel_ids = self.url_size_varselids(response)
        selected_size = self.product_dropdown_size(response)

        requests = []
        if selected_size:
            dropdown_ids = response.xpath('//section[input[@name="varselid[2]"]]//option/@value').extract()
            for color_varsel_id in color_varsel_ids:
                for dropdown_id in dropdown_ids:
                    for size_varsel_id in size_varsel_ids:
                        url_params = {
                            'anid': self.url_anid(response),
                            'cl': self.url_cl(response),
                            'varselid[0]': color_varsel_id,
                            'varselid[1]': size_varsel_id,
                            'varselid[2]': dropdown_id
                        }
                        requests.append(self.sku_url_request(response, url_params))
            return requests
        for color_varsel_id in color_varsel_ids:
            for size_varsel_id in size_varsel_ids:
                url_params = {
                    'anid': self.url_anid(response),
                    'cl': self.url_cl(response),
                    'varselid[0]': color_varsel_id,
                    'varselid[1]': size_varsel_id
                }
                requests.append(self.sku_url_request(response, url_params))
        return requests

    def sku_url_request(self, response, url_params):
        base_url = re.findall('(.*?\?)', response.url)
        url = "{}{}".format(base_url[0], urlencode(url_params))
        return Request(url=url, callback=self.parse_skus)

    def url_anid(self, response):
        url_anid = response.xpath('//script[contains(text(), "window.ads.artNr =")]')\
                   .re('window.ads.artNr = \'(.*?)\'\;')
        return url_anid[0].strip()

    def url_cl(self, response):
        url_cl = response.xpath('//script[contains(text(), "window.ads.cl =")]').re('window.ads.cl = \'(.*?)\'\;')
        return url_cl[0].strip()

    def url_color_varselids(self, response):
        return response.css(".colorspots__item::attr(data-varselid)").extract()

    def url_size_varselids(self, response):
        return response.css(".sizespots__item::attr(data-varselid)").extract()

    def product_name(self, response):
        return response.css('h1[itemprop="name"]::text').extract_first().strip()

    def product_pricing(self, response):
        current_price = response.css('.product__price__current').re('([\d]+,[\d]+)')
        raw_pre_price = response.css('.product__price__wrong').re('([\d]+,[\d]+)')

        previous_prices = [int(float(pre_price.replace(",", ".")) * 100) for pre_price in raw_pre_price]
        return int(float(current_price[0].replace(",", ".")) * 100), previous_prices

    def product_currency(self, response):
        raw_currency = response.css('.product__price__current::text').extract_first().strip()[-1]
        return self.currency_map.get(raw_currency)

    def product_category(self, response):
        return self.clean(response.css('.breadcrumb__item ::text').extract())

    def product_brand(self, response):
        return response.css('title::text').extract_first().split("|")[1].strip()

    def image_urls(self, response):
        image_css = '[class="p-details__image__thumb__container"] a::attr(href)'
        raw_image_urls = response.css(image_css).extract()
        image_urls = [response.urljoin(image_url) for image_url in raw_image_urls]

        return self.clean(image_urls)

    def product_retailer_sku(self, response):
        return response.css(".js-artNr::text").extract_first().strip()

    def product_description(self, response):
        description = response.css('[itemprop="description"] ::text').extract()
        description.extend(response.css('.details__box--detailsAdd div td::text').extract())
        return self.clean(description)

    def product_care(self, response):
        care = response.css('.p-details__material ::text').extract()
        care.extend(response.css('div.p-details__careSymbols ::text').extract())
        return self.clean(care)

    def product_colour(self, response):
        return response.css(".cj-active::attr(title)").extract_first().strip()

    def product_size(self, response):
        size = response.xpath("//div[contains(@class,'item--active at-dv-size-button')]/text()").extract_first()
        if not size:
            size = response.xpath("//div[contains(@class,'item--disabled')]/text()").extract_first()
        return size.strip()

    def product_outofstock(self, response):
        out_of_stock = response.css("div[itemprop='offers'] span::text").extract_first()
        return not ('ver' in out_of_stock)

    def product_dropdown_size(self, response):
        dropdown_selected_xpath = '//section[input[@name="varselid[2]"]]//option[@selected="selected"]/text()'
        return response.xpath(dropdown_selected_xpath).extract_first()

    def clean(self, to_clean):
        cleaned = [per_entry.strip() for per_entry in to_clean] if to_clean else ""
        return list(filter(None, cleaned))
