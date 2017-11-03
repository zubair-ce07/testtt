# coding=utf-8
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FarnellSpider(CrawlSpider):
    name = 'farnell_spider'
    allowed_domains = ['farnell.com']
    start_urls = ['http://uk.farnell.com/']

    allowed_categories_re = [
        '/wireless-modules-adaptors$',
        '/engineering-software$',
        '/electrical$'
    ]
    listing_css = ['.categoryList nav.filterCategoryLevelOne']
    paging_css = ['.paginLinks .paginNextArrow']

    rules = (
        Rule(LinkExtractor(restrict_css='li[role="menuitem"]', allow=allowed_categories_re)),
        Rule(LinkExtractor(restrict_css=listing_css + paging_css)),
        Rule(LinkExtractor(restrict_css='#sProdList .productImage'), callback='parse_product'),
    )

    def parse_product(self, response):

        product = {}
        product['url'] = response.url
        product['title'] = self.title(response)
        product['unit_price'] = self.unit_price(response)

        product['brand'], product['manufacturer'] = self.brand_and_manufacturer(response)
        product['manufacturer_part'] = self.manufacturer_part(response)

        product['overview'] = self.overview(response)
        product['information'] = self.information(response)

        product['origin_country'] = self.origin_country(response)
        product['tariff_number'] = self.tariff(response)

        product['files'] = self.files(response)
        product['file_urls'] = self.file_urls(response)

        product['primary_image_url'] = self.primary_image_url(response)
        product['trail'] = self.trail(response)

        yield product

    def title(self, response):
        return response.css('#productMainImage::attr(alt)').extract_first()

    def brand_and_manufacturer(self, response):
        brand_manufacture_xpath_t = '//*[@class="proDescAndReview"]//*[contains(@itemprop,"{0}")]//text()'
        brand = response.xpath(brand_manufacture_xpath_t.format('brand')).extract_first()
        manufacturer = response.xpath(brand_manufacture_xpath_t.format('manufacturer')).extract_first()
        return brand, manufacturer

    def manufacturer_part(self, response):
        part = response.css('[itemprop=mpn]::text').extract_first()
        return part.strip() if part else None

    def unit_price(self, response):
        price = response.css('[itemprop=price]::text').extract_first()
        if price:
            return float(price.strip())

    def overview(self, response):
        overview = response.css('#pdpSection_FAndB .collapsable-content ::text').extract()
        return " ".join(clean(overview))

    def information(self, response):
        xpath_prefix = '//*[@id="pdpSection_pdpProdDetails"]'
        names = response.xpath(xpath_prefix + '//dt[contains(@id,"descAttributeName")]//label//text()').extract()
        values = response.xpath(xpath_prefix + '//dd[contains(@id,"descAttributeValue")]//a//text()').extract()
        information = []
        for name, value in zip(names, values):
            information.append({'name': name, 'value': value})
        return information

    def origin_country(self, response):
        xpath = '//*[@id="pdpSection_ProductLegislation"]//dt[contains(.,"Country of Origin:")]/following::dd[1]/text()'
        country = clean(response.xpath(xpath).extract())
        return country[0] if country else None

    def tariff(self, response):
        xpath = '//*[@id="pdpSection_ProductLegislation"]//dt[contains(.,"Tariff No:")]/following::dd[1]/text()'
        tariff = clean(response.xpath(xpath).extract())
        return tariff[0] if tariff else None

    def files(self, response):
        filenames = response.css('#technicalData a::text').extract()
        return clean(filenames)

    def file_urls(self, response):
        return response.css('#technicalData a::attr(href)').extract()

    def primary_image_url(self, response):
        return response.css('#productMainImage::attr(data-full)').extract_first()

    def trail(self, response):
        breadcrumbs = response.css('#breadcrumb nav[role="navigation"] a::text').extract()
        return breadcrumbs[1:-1]


def clean(to_clean):
    if isinstance(to_clean, str):
        return sanitize(to_clean)
    elif isinstance(to_clean, list):
        cleaned = [sanitize(x) for x in to_clean]
        return [x for x in cleaned if x]
    return to_clean


def sanitize(string_input):
    result = re.sub('\s+', ' ', string_input)
    return result.strip()
