import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCerca(BaseMixinPPE):
    name = property_slug = 'cerca'
    allowed_domains = [
        'cerca.prospectportal.com',
        'cercaatsdsu.com'
    ]

    login_domain = 'https://cerca.prospectportal.com/'
    site_domain = 'http://www.cercaatsdsu.com/'

    property_name = 'Cerca'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCerca(PPBaseParseSpiderE, MixinCerca):
    name = MixinCerca.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return f"Studio-Cerca {name}"
        return f"{room_name}-Cerca {name}"


class CrawlSpiderCerca(MixinCerca, PPBaseCrawlSpiderE):
    amenities_css = ".amen-grid-row"
    contact_info_css = "title::text"
    p_images_css = ".bwg_lightbox ::attr(href)"
    description_css = ".amen-wrap article::text"
    name = MixinCerca.name + '-crawl'
    parse_spider = ParseSpiderCerca()
    deal_x = '//div[@class="specialSlider"]//span/text()'
    r_images_percentage = (20 / 100)

    def parse_contact(self, response):
        ps = self.parse_spider
        title = clean(response.css(self.contact_info_css))[0]
        ps.contact_info = re.findall('(\d+\-\d+\-\d+)', title)[0]
        ps.p_desc = clean(response.css(self.description_css))
        ps.deals = clean(response.xpath(self.deal_x))

    def parse_amenities(self, response):
        ps = self.parse_spider
        lst = response.css(self.amenities_css)
        ps.p_amenities = clean(lst[0].css('li::text'))
        ps.r_amenities = clean(lst[1].css('li::text'))
        self.parse_images(response)

    def parse_images(self, response):
        ps = self.parse_spider
        images = clean(response.css(self.p_images_css))
        r_images_count = self.r_images_percentage * float(len(images))
        r_images = images[0: int(r_images_count)]
        ps.r_photos += [response.urljoin(image) for image in r_images if image]
        ps.p_images += set(images) - set(r_images)