import scrapy
import re
import json
from urllib.parse import urljoin
from schwab.items import SchwabItem


class Schwab(scrapy.Spider):
    name = "schwab_crawler"
    start_urls = ["https://www.schwab.de/"]
    product_api_url = "https://www.schwab.de/index.php?"
    sub_categories_api = "https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true&staticContent=true&cacheID="

    def parse(self, response):
        sub_categories_content = response.xpath('//script[contains(text(),"window.general.navi.cacheID")]/text()') \
            .extract_first()
        sub_categories_id = re.search("\d[0-9]{9}", sub_categories_content)
        sub_categories_id = sub_categories_id.group()
        content_url = self.sub_categories_api + sub_categories_id
        yield scrapy.Request(url=content_url, callback=self.sub_categories_urls)

    def sub_categories_urls(self, response):
        json_content = json.loads(response.body.decode())
        for i in json_content:
            for j in i['sCat']:
                sub_categories_url = j.get("url")
                yield scrapy.Request(url=sub_categories_url, dont_filter=True, callback=self.parse_sub_categories)

    def next_pages(self, response):
        next_page_url = response.xpath('.//span[@class="paging__btn"]//a/@href').extract_first()
        if next_page_url:
            return urljoin(response.url, next_page_url)

    def parse_sub_categories(self, response):
        product_ids = response.xpath('.//a[@class="at-pl-see-details btn-text js-pl-product"]/@href').extract()
        for product_id in product_ids:
            product_url = urljoin(response.url, product_id)
            yield scrapy.Request(url=product_url, dont_filter=True, callback=self.parse_product)
        if self.next_pages(response):
            yield scrapy.Request(url=self.next_pages(response), callback=self.parse_sub_categories)

    def product_title(self, response):
        return response.xpath('.//span[@itemprop="name"]/text()').extract_first().strip()

    def article_no(self, response):
        return response.xpath('.//span[@class="js-artNr at-dv-artNr"]/text()').extract_first().strip()

    def product_description(self, response):
        return self.clean_list(response.xpath('.//div[@itemprop="description"]/text()').extract())

    def care_and_description(self, response):
        product_care = response.xpath('.//ul[@class="l-outsp-bot-5"]//li/text()').extract()
        return self.clean_list(product_care) + self.product_description(response)

    def product_features(self, response):
        feature_keys = self.clean_list(response.xpath('.//td[@class="left"]//span/text()').extract())
        feature_values = self.clean_list(response.xpath('.//td/text()').extract())
        features = {}
        for item in zip(feature_keys, feature_values):
            features[item[0]] = item[1]
        return features

    def image_urls(self, response):
        return response.xpath('.//a[@id="magic"]/@href').extract()

    def sku_old_price(self, response):
        return self.clean_list(response.xpath('.//div[@class="pricing__norm--wrong"]//span/text()').extract())

    def sku_price(self, response):
        return response.xpath('.//span[@class="js-detail-price"]/text()').extract_first().strip()

    def sku_color(self, response):
        sku_color = response.xpath('.//input[@class="js-current-color-name"]/@value').extract_first()
        if sku_color:
            return sku_color.strip()
        else:
            return response.xpath('.//span[@class="js-color-value at-dv-color"]//b/text()').extract_first()

    def sku_size(self, response):
        return response.xpath('.//input[@class="js-current-size-name"]/@value').extract_first()

    def sku_id(self, response):
        return response.xpath('.//input[@name="aid"]/@value').extract_first()

    def sku_currency(self, response):
        return response.xpath('.//meta[@itemprop="priceCurrency"]/@content').extract_first()

    def sku_variant(self, response):
        return response.xpath('.//input[@class="js-current-variant-name"]/@value').extract_first()

    def skus(self, response):
        sku = {}
        sku_id = self.sku_id(response)
        sku["old_price"] = self.sku_old_price(response)
        sku["new_price"] = self.sku_price(response)
        sku["color"] = self.sku_color(response)
        sku["size"] = self.sku_size(response)
        sku["currency"] = self.sku_currency(response)
        sku["variant"] = self.sku_variant(response)
        return {sku_id: sku}

    def parse_product(self, response):
        item = SchwabItem()
        item["skus"] = {}
        item["title"] = self.product_title(response)
        item["retailer_sku"] = self.article_no(response)
        item["care_and_description"] = self.care_and_description(response)
        item["features"] = self.product_features(response)
        item["image_urls"] = self.image_urls(response)
        item["categories"] = self.categories_path(response)
        item["url"] = response.url
        item["meta"] = {"requests": self.main_request(response, item), }
        return self.request_or_item(item)

    def parent_id(self, response):
        return response.xpath('.//input[@name="parentid"]/@value').extract_first()

    def language(self, response):
        return response.xpath('.//input[@name="lang"]/@value').extract_first()

    def categories_path(self, response):
        return self.clean_list(response.xpath('.//span[@itemprop="name"]/text()').extract()[2:-1])

    def econdapath(self, response):
        econdapath = self.categories_path(response)
        return '/'.join(econdapath)

    def form_data_cl(self, response):
        return response.xpath('.//input[@name="cl"]/@value').extract()[3]

    def actcontrol(self, response):
        return response.xpath('.//input[@name="actcontrol"]/@value').extract()[1]

    def promo(self, response):
        new_promo = []
        for promo in self.anids(response):
            new_promo.append(promo.split("-")[3])
        return new_promo

    def art_name(self, response):
        return response.xpath('//input[@ name="artName"]/@value').extract_first()

    def anids(self, response):
        json_content = response.xpath('//script[contains(text(),"articlesString")]/text()').extract_first()
        anid_content = re.findall('\d+\|\d+\|[A-Za-z0-9]+\|(?:[A-Za-z0-9]+,[A-Za-z0-9]+|[A-Za-z0-9]+)', json_content)
        parent_id = self.parent_id(response)
        anids = []
        for i in anid_content:
            anids.append((parent_id+"-"+i.split('|')[1])+"-"+(i.split('|')[3])+"-"+(i.split('|')[2]))
        return anids

    def art_nr(self, response):
        art_nr = []
        for i in self.anids(response):
            art_nr.append((i.split('-')[1])+(i.split('-')[3]))
        return art_nr

    def color_ids(self, response):
        available_colors = response.xpath(
            './/div[@class="c-colorspots colorspots--inlist"]//a/@data-varselid').extract()
        if available_colors:
            return available_colors

    def size_ids(self, response):
        available_sizes = response.xpath('.//div[@class="l-outsp-bot-5"]//button/@data-varselid').extract()
        if available_sizes:
            return available_sizes
        else:
            return response.xpath('//select[@name="variant"]//option/@value').extract()[1:]

    def product_fits(self, response):
        return response.xpath('.//select[@name="variant"]/option/@value').extract()[1:]

    def fit_exist_or_not(self, response):
        return response.xpath('//select[@class="variants js-variantSelector js-moreinfo-variant js-sh-dropdown "]'
                              '/option/@value').extract()[1:]

    def size_color_fit_content(self, response):
        if self.fit_exist_or_not(response):
            if self.color_ids(response):
                sizes = len(self.color_ids(response))*len(self.product_fits(response))
                if sizes:
                    available_sizes = len(self.anids(response))/sizes
                    colors = self.color_ids(response) * len(self.product_fits(response)) * int(available_sizes)
                    fits = self.product_fits(response) * len(self.color_ids(response)) * int(available_sizes)
                    return colors, fits
            else:
                if self.size_ids(response):
                    available_sizes = len(self.anids(response))/len(self.product_fits(response))
                    fits = self.product_fits(response)*int(available_sizes)
                    return fits

                else:
                    return self.fit_exist_or_not(response)
        if self.color_ids(response):
            if self.size_ids(response):
                available_sizes = float(len(self.anids(response))/len(self.color_ids(response)))
                return self.color_ids(response) * int(available_sizes)

    def available_sizes(self, response):
        available_sizes = []
        for anid in self.anids(response):
            available_sizes.append(anid.split("-")[2])
        return available_sizes

    def varselid_key(self, response):
        return response.xpath('//input[@class="js-varselid-COLOR js-varselid"]/@name').extract_first()

    def fit_key(self, response):
        return response.xpath('//div[@class=" details__variation js-variantSelector variant clearfix l-outsp-bot-20"]'
                              '//input/@name').extract_first()

    def varselid_value(self, response):
        return response.xpath('//input[@class="js-varselid-COLOR js-varselid"]/@value').extract_first()

    def special_anids(self, response):
        anids = []
        for i in self.anids(response):
            garbage_value = i.split('-')[2]
            if garbage_value == '0':
                anids.append(self.parent_id(response)+"-"+i.split('-')[1]+"-"+i.split('-')[3])
            else:
                anids.append((self.parent_id(response)+"-"+i.split('-')[1])+"-"+(i.split('-')[3])+"-"+(i.split('-')[2]))
        return anids

    def forced_sizes(self, response):
        forced_sizes = []
        for size in self.available_sizes(response):
            forced_size = response.xpath('.//div[@class="l-outsp-bot-5"]'
                                         '//button[@data-noa-size="'+size+'"]/@data-selection-id').extract_first()
            if forced_size:
                forced_sizes.append(forced_size)
            else:
                forced_sizes.append(response.xpath('//select[@name="variant"]'
                                                   '//option[@data-noa-size="'+size+'"]/@value').extract_first())
        return forced_sizes

    def fit_size_requests(self, response, item):
        multiple_requests = []
        for anid, size, fit in zip(self.anids(response), self.fit_exist_or_not(response),
                                   self.size_color_fit_content(response)):
            form_data = {
                self.fit_key(response): fit,
                self.varselid_key(response): self.varselid_value(response),
                'cl': self.form_data_cl(response),
                'forcedSize': size,
                'varselid[0]': size,
                'econdapath': self.econdapath(response),
                'anid': anid,
            }
            request = scrapy.FormRequest(url=self.product_api_url, formdata=form_data,
                                         meta={"item": item},
                                         callback=self.parse_main_request, dont_filter=True)
            multiple_requests.append(request)
        return multiple_requests

    def fit_request(self, response, item):
        multiple_requests = []
        for anid, size in zip(self.anids(response), self.fit_exist_or_not(response)):
            form_data = {
                self.varselid_key(response): self.varselid_value(response),
                'cl': self.form_data_cl(response),
                'forcedSize': size,
                'varselid[0]': size,
                'econdapath': self.econdapath(response),
                'anid': anid,
            }
            request = scrapy.FormRequest(url=self.product_api_url, formdata=form_data,
                                         meta={"item": item},
                                         callback=self.parse_main_request, dont_filter=True)
            multiple_requests.append(request)
        return multiple_requests

    def color_size__fit_requests(self, response, item):
        multiple_requests = []
        color, fits = self.size_color_fit_content(response)
        for anid, color, fit, size, promo, artnr in zip(self.anids(response), color, fits,
                                                        self.forced_sizes(response), self.promo(response),
                                                        self.art_nr(response)):
            form_data = {
                self.varselid_key(response): color,
                self.fit_key(response): fit,
                'cl': self.form_data_cl(response),
                'econdapath': self.econdapath(response),
                'anid': anid,
                'aid': anid,
                'forcedSize': size,
                'varselid[0]': size,
                'actcontrol': self.actcontrol(response),
                'parentid': self.parent_id(response),
                'artName': self.art_name(response),
                'artNr': artnr,
                'lang': self.language(response),
                'promo': promo,
            }
            request = scrapy.FormRequest(url=self.product_api_url, formdata=form_data, meta={"item": item},
                                         dont_filter=True, callback=self.parse_main_request)
            multiple_requests.append(request)
        return multiple_requests

    def color_size_request(self, response, item):
        multiple_requests = []
        for anid, color, size, promo, artnr in zip(self.anids(response), self.size_color_fit_content(response),
                                                   self.forced_sizes(response), self.promo(response),
                                                   self.art_nr(response)):
            form_data = {
                self.varselid_key(response): color,
                'cl': self.form_data_cl(response),
                'econdapath': self.econdapath(response),
                'artnumsofsizes': artnr,
                'anid': anid,
                'aid': anid,
                'forcedSize': size,
                'varselid[0]': size,
                'actcontrol': self.actcontrol(response),
                'parentid': self.parent_id(response),
                'artName': self.art_name(response),
                'artNr': artnr,
                'lang': self.language(response),
                'promo': promo,
            }
            request = scrapy.FormRequest(url=self.product_api_url, formdata=form_data, meta={"item": item},
                                         callback=self.parse_main_request, dont_filter=True)
            multiple_requests.append(request)
        return multiple_requests

    def size_requests(self, response, item):
        multiple_requests = []
        for anid, size, promo, artnr in zip(self.anids(response), self.forced_sizes(response),
                                            self.promo(response), self.art_nr(response)):
            form_data = {
                self.varselid_key(response): self.varselid_value(response),
                'cl': self.form_data_cl(response),
                'econdapath': self.econdapath(response),
                'anid': anid,
                'aid': anid,
                'forcedSize': size,
                'varselid[0]': size,
                'actcontrol': self.actcontrol(response),
                'parentid': self.parent_id(response),
                'artName': self.art_name(response),
                'artNr': artnr,
                'lang': self.language(response),
                'promo': promo,
            }
            request = scrapy.FormRequest(url=self.product_api_url, formdata=form_data, meta={"item": item},
                                         callback=self.parse_main_request, dont_filter=True)
            multiple_requests.append(request)
        return multiple_requests

    def color_requests(self, response, item):
        multiple_requests = []
        for anid, color in zip(self.special_anids(response), self.color_ids(response)):
            form_data = {
                self.varselid_key(response): color,
                'cl': self.form_data_cl(response),
                'ajaxdetails': 'adsColorChange',
                'econdapath': self.econdapath(response),
                'anid': anid,
                'loadDataPartially': 'true'
            }
            request = scrapy.FormRequest(url=self.product_api_url, formdata=form_data, meta={"item": item},
                                         callback=self.parse_main_request, dont_filter=True)
            multiple_requests.append(request)
        return multiple_requests

    def main_request(self, response, item):
        if self.size_color_fit_content(response):
            if self.fit_exist_or_not(response):
                if isinstance(self.size_color_fit_content(response), list):
                    if self.size_ids(response):

                        return self.fit_size_requests(response, item)
                    else:

                        return self.fit_request(response, item)

                elif isinstance(self.size_color_fit_content(response), tuple):
                    
                    return self.color_size__fit_requests(response, item)
            else:
                return self.color_size_request(response, item)

        elif self.size_ids(response):
            return self.size_requests(response, item)

        elif self.color_ids(response):
            return self.color_requests(response, item)
        else:
            item['skus'].update(self.skus(response))

    def parse_main_request(self, response):
        item = response.meta["item"]
        item["skus"].update(self.skus(response))
        return self.request_or_item(item)

    def clean_list(self, my_list):
        final_list = []
        for entry in my_list:
            entry = entry.strip()
            if entry and entry not in final_list:
                final_list.append(entry)
        return final_list

    def request_or_item(self, item):
        if item["meta"]["requests"]:
            return item["meta"]["requests"].pop()
        else:
            del item["meta"]
            return item