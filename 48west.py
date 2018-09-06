import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class Mixin48West(BaseMixinPPE):
    name = property_slug = '48-west'
    allowed_domains = [
        'liveat48west.prospectportal.com',
        '48west.com'
    ]

    login_domain = 'https://liveat48west.prospectportal.com/'
    site_domain = 'http://www.48west.com/'

    property_name = '48 West'
    landlord_name = 'Asset Campus Housing'
    floor_amenities_url_t = '{}/gallery'


class ParseSpider48West(PPBaseParseSpiderE, Mixin48West):
    name = Mixin48West.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = re.sub('(\d+\.?\d?)x(\d+\.?\d?)\s?(.*)', '\\1 Bedroom \\2 Bathroom \\3', name)
        return room_name


class CrawlSpider48West(Mixin48West, PPBaseCrawlSpiderE):
    p_amenities_css = ".amenities-items .right-section strong::text"
    contact_info_xpath = "//a[@title='Call Now']/text()"
    amenities_photos_xpath = "//a[@data-lightbox='01-Amenities']/@href"
    exterior_photos_xpath = '//a[@data-lightbox="02-Exterior"]/@href'
    style_photos_xpath = '//a[@data-lightbox="04-Lifestyle"]/@href'
    r_photos_xpath = "//a[@data-lightbox='03-Interior']/@href"
    description_css = ".index-main-content.post-content p"
    name = Mixin48West.name + '-crawl'
    parse_spider = ParseSpider48West()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'

    def parse_contact(self, response):
        ps = self.parse_spider
        ps.contact_info += clean(response.xpath(self.contact_info_xpath))
        desc_sel = response.css(self.description_css)
        ps.p_desc = clean(desc_sel[0].css("::text"))
        ps.p_desc += clean(desc_sel[1].css("::text"))

    def parse_amenities(self, response):
        ps = self.parse_spider
        ps.p_amenities += clean(response.css(self.p_amenities_css))

    def parse_floor_amenities(self, response):
        ps = self.parse_spider
        ps.r_photos = [response.urljoin(url) for url in clean(response.xpath(self.r_photos_xpath))]
        ps.p_images = [response.urljoin(url) for url in clean(response.xpath(self.amenities_photos_xpath))]
        ps.p_images += [response.urljoin(url) for url in clean(response.xpath(self.exterior_photos_xpath))]
        ps.p_images += [response.urljoin(url) for url in clean(response.xpath(self.style_photos_xpath))]