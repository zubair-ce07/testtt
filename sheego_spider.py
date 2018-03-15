import scrapy
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlencode

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

    currency = {
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

        urls = self.sku_urls(response)
        if urls:
            yield scrapy.Request(url=urls[0], callback=self.skus, meta={'item': item, 'urls': urls})
        else:
            yield item

    def skus(self, response):
        item = self.sku(response)
        urls = response.meta['urls']
        urls.pop(0)
        if urls:
            yield scrapy.Request(url=urls[0], callback=self.skus, meta={'item': item, 'urls': urls})
        else:
            yield item

    def sku(self, response):
        item = response.meta['item']

        color = self.product_colour(response)
        size = self.product_size(response)
        price, previous_prices = self.product_prices(response)
        dropdown_size = self.product_dropdown_size(response)

        out_of_stock = 'verfügbar' in self.product_outofstock(response)
        sku = {
            'price': price,
            'previous_price': previous_prices,
            'size': size,
            'color': color,
            'sku_id': "{}_{}".format(color, size)
        }
        if out_of_stock:
            sku['out_of_stock'] = out_of_stock
        if dropdown_size:
            sku['sku_id'] = "{}_{}/{}".format(color, dropdown_size.strip(), size)
            sku['size'] = "{}/{}".format(dropdown_size.strip(), size)

        item['skus'].append(sku)
        return item

    def sku_urls(self, response):
        color_varsel_ids = self.url_color_varselids(response)
        size_varsel_ids = self.url_size_varselids(response)

        dropdown_selected_xpath = "//select[contains(@class, 'form-group--select form-group--select--big " \
                                  "js-sh-dropdown l-mb-10 js-variant-select')]/option[@selected='selected']/text()"
        selected_size = response.xpath(dropdown_selected_xpath).extract_first()

        urls = []
        if selected_size:
            dropdown_ids_xpath = "//select[contains(@class, 'form-group--select form-group" \
                                   "--select--big js-sh-dropdown l-mb-10 js-variant-select')]/option/@value"
            dropdown_ids = response.xpath(dropdown_ids_xpath).extract()
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
                        urls.append(self.sku_url(response, url_params))
        else:
            for color_varsel_id in color_varsel_ids:
                for size_varsel_id in size_varsel_ids:
                    url_params = {
                        'anid': self.url_anid(response),
                        'cl': self.url_cl(response),
                        'varselid[0]': color_varsel_id,
                        'varselid[1]': size_varsel_id
                    }
                    urls.append(self.sku_url(response, url_params))
        return urls

    def sku_url(self, response, url_params):
        base_url = re.findall('(.*?\?)', response.url)
        return "{}{}".format(base_url[0], urlencode(url_params))

    def url_anid(self, response):
        url_anid = response.xpath('//script[contains(text(), "window.ads.artNr =")]').re('window.ads.artNr = \'(.*?)\'\;')
        return url_anid[0].strip()

    def url_cl(self, response):
        url_cl = response.xpath('//script[contains(text(), "window.ads.cl =")]').re('window.ads.cl = \'(.*?)\'\;')
        return url_cl[0].strip()

    def url_color_varselids(self, response):
        return response.xpath("//span[@class='colorspots__wrapper']/span/@data-varselid").extract()

    def url_size_varselids(self, response):
        varselid_xpath = "//div[contains(@class, 'btn sizespots__item js-click-variant')]/@data-varselid"
        return response.xpath(varselid_xpath).extract()

    def product_name(self, response):
        return response.xpath('//h1[contains(@itemprop, "name")]//text()').extract_first().strip()

    def product_prices(self, response):
        current_price_xpath = '//span[contains(@class, "product__price__current")]//text()'
        previous_price_xpath = '//span[contains(@class, "product__price__wrong")]//text()'

        current_price = response.xpath(current_price_xpath).re('([\d]+,[\d]+)')
        raw_pre_price = response.xpath(previous_price_xpath).re('([\d]+,[\d]+)')

        previous_price = [int(float(raw_pre_price[0].replace(",", ".")) * 100)] if raw_pre_price else []
        return int(float(current_price[0].replace(",", ".")) * 100), previous_price

    def product_currency(self, response):
        currency_xpath = '//span[contains(@class, "product__price__current")]//text()'
        raw_currency = response.xpath(currency_xpath).extract_first().strip()[-1]
        return self.currency.get(raw_currency)

    def product_category(self, response):
        return self.clean(response.xpath('//span[contains(@class, "breadcrumb__item")]//text()').extract())

    def product_brand(self, response):
        return response.css('title::text').extract_first().split("|")[1].strip()

    def image_urls(self, response):
        image_xpath = '//div[contains(@class, "p-details__image__thumb__container")]/a/@href'
        raw_image_urls = response.xpath(image_xpath).extract()
        image_urls = [response.urljoin(image_url) for image_url in raw_image_urls]

        return self.clean(image_urls)

    def product_retailer_sku(self, response):
        return response.css('span.js-artNr.at-dv-artNr::text').extract_first().strip()

    def product_description(self, response):
        description_xpath = '//div[contains(@itemprop , "description")]//text()'
        description = response.xpath(description_xpath).extract()

        description_css = 'div.f-xs-12.f-md-6.l-hidden.l-visible-md table ::text'
        description.extend(response.css(description_css).extract())

        return self.clean(description)

    def product_care(self, response):
        care_css = 'p.l-subline.l-mb-20.l-hidden.l-visible-md+ table tbody ::text'
        care = response.css(care_css).extract()

        symbols_xpath = '//div[contains(@class, "p-details__careSymbols")]//text()'
        care.extend(response.xpath(symbols_xpath).extract())

        return self.clean(care)

    def product_colour(self, response):
        active_colour_xpath = "//span[@class='colorspots__wrapper']/span[contains(@class, 'cj-active')]/@title"
        return response.xpath(active_colour_xpath).extract_first().strip()

    def product_size(self, response):
        size = response.xpath("//div[contains(@class,'item--active at-dv-size-button')]/text()").extract_first()
        if not size:
            size = response.xpath("//div[contains(@class,'item--disabled')]/text()").extract_first()
        return size.strip()

    def product_outofstock(self, response):
        return response.xpath("//div[@itemprop='offers']/*/text()").extract_first()

    def product_dropdown_size(self, response):
        dropdown_selected_xpath = "//select[contains(@class, 'form-group--select form-group--select--big " \
                                  "js-sh-dropdown l-mb-10 js-variant-select')]/option[@selected='selected']/text()"
        return response.xpath(dropdown_selected_xpath).extract_first()

    def clean(self, to_clean):
        cleaned = [per_entry.strip() for per_entry in to_clean] if to_clean else ""
        return list(filter(None, cleaned))
