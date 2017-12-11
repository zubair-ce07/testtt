import scrapy
import re
from tutorial.product import Product
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from collections import deque

class FarnellSpider(CrawlSpider):
    # name of spider
    name = 'farnell'

    # list of allowed domains
    allowed_domains = ['uk.farnell.com']
    # starting url
    start_urls = ['http://uk.farnell.com/altium/07-200-103-804-05-1/ide-arm-node-locked-cortex-m/dp/2523301',
                  'http://uk.farnell.com/pro-elec/2118-2m/extension-lead-2way-2m/dp/1286464',
                  'http://uk.farnell.com/mk/1161whi/ceiling-rose-4-terminal/dp/7218278',
                  'http://uk.farnell.com/pro-elec/83320/batten-lampholder-ho-skirt-t2/dp/1394790']
    # location of csv file
    custom_settings = {'FEED_URI': 'tmp/farnell.json'}

    def parse(self, response):
        # Extract product information

        product = Product()
        product['url'] = response.url
        product['title'] = self.title(response)
        price = self.unit_price(response)
        if price:
            product['unit_price'] = price

        overview = self.overview(response)
        if overview:
            product['overview'] = overview

        product['information'] = self.information(response)
        manufacturer = self.manufacturer(response)
        if manufacturer:
            product['manufacturer'] = manufacturer

        m_p = self.manufacturer_part(response)
        if m_p:
            product['manufacturer_part'] = m_p

        product['origin_country'] = self.origin_country(response)

        tariff, value = self.tariff(response)
        if tariff and 'Tariff' in tariff:
            product['tariff_number'] = value.strip()

        product['files'] = self.files(response)
        product['file_urls'] = self.file_urls(response)

        product['primary_image_url'] = self.primary_image_url(response)

        product['trail'] = self.trail(response)

        yield product

    @staticmethod
    def title(response):
        title = response.css('.imgCont > img::attr(alt)').extract_first()
        return title

    @staticmethod
    def unit_price(response):
        price = response.css('.productPrice > span.price::text').extract_first()
        if price:
            price = price.strip()
            return price

    @staticmethod
    def overview(response):
        overview_container = response.css('#pdpSection_FAndB')
        overview = overview_container.css('.contents::text').extract()
        return overview

    @staticmethod
    def information(response):
        c = response.css('#pdpSection_pdpProdDetails')
        headings = c.css('.collapsable-content > dl > dt > label::text').extract()
        details = c.css('.collapsable-content > dl > dd > a::text').extract()
        information = {}
        for item in zip(headings, details):
            information[item[0]] = item[1]
        return information

    @staticmethod
    def manufacturer(response):
        manufacturer = response.css('.brandLogo > dd > span::text').extract_first()
        return manufacturer

    @staticmethod
    def manufacturer_part(response):
        m_p = response.css('[itemprop=mpn]::text').extract_first().strip()
        return m_p

    @staticmethod
    def origin_country(response):
        legis_container = response.css('#pdpSection_ProductLegislation')
        country = legis_container.css('.collapsable-content > dl > dd::text').extract_first()
        return country.strip()

    @staticmethod
    def tariff(response):
        legis_container = response.css('#pdpSection_ProductLegislation')
        legis = legis_container.css('.collapsable-content > dl > dd::text').extract_first()
        tariff = legis_container.css('.collapsable-content > dl > dt > strong::text').extract_first()
        return tariff, legis[1]

    @staticmethod
    def files(response):
        return response.css('#technicalData > li > a::attr(title)').extract()

    @staticmethod
    def file_urls(response):
        return response.css('#technicalData > li > a::attr(href)').extract()

    @staticmethod
    def primary_image_url(response):
        return response.css('#productMainImage::attr(src)').extract()

    @staticmethod
    def trail(response):
        breadcrumbs = response.css('.nav li > a::text').extract()
        category = breadcrumbs[1:]
        return category

