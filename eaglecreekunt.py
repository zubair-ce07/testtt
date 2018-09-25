import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinEagleCreek(BaseMixinPPE):
    name = property_slug = 'eagle-creek'
    allowed_domains = [
        'eaglecreekapts.prospectportal.com',
        'eaglecreekunt.com'
    ]

    login_domain = 'https://eaglecreekapts.prospectportal.com/'
    site_domain = 'https://www.eaglecreekunt.com/'

    property_name = 'Eagle Creek'
    landlord_name = 'Asset Campus Housing'
    floor_amenities_url_t = '{}/gallery/'


class ParseSpiderEagleCreek(PPBaseParseSpiderE, MixinEagleCreek):
    name = MixinEagleCreek.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)x(\d+)\s?(.*)', '\\1 Bedroom \\2 Bathroom-The\\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return  room_name


class CrawlSpiderEagleCreek(MixinEagleCreek, PPBaseCrawlSpiderE):
    amenities_css = ".ul-nopadding"
    contact_info_css = ".footer-mobile ::text"
    p_images_css = "#home-slider img::attr(src)"
    description_css = ".amanities_block .block-content p::text"
    name = MixinEagleCreek.name + '-crawl'
    parse_spider = ParseSpiderEagleCreek()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
    r_images_percentage = (30 / 100)

    def parse_contact(self, response):
        ps = self.parse_spider
        ps.contact_info = clean(response.css(self.contact_info_css))
        ps.p_desc = clean(response.css(self.description_css))

    def parse_amenities(self, response):
        ps = self.parse_spider
        lst = response.css(self.amenities_css)
        ps.p_amenities = clean(lst[0].css('li::text'))
        ps.r_amenities = clean(lst[1].css('li::text'))

    def parse_floor_amenities(self, response):
        ps = self.parse_spider
        images = clean(response.css(self.p_images_css))
        r_images_count = self.r_images_percentage * float(len(images))
        r_images = images[0: int(r_images_count)]
        ps.r_photos = [response.urljoin(image) for image in r_images if image]
        ps.p_images = set(images) - set(r_images)
