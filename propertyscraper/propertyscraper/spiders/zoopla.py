import re
from dateutil import parser
import datetime
from collections import OrderedDict
import pdb

from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from propertyscraper.items import PropertyscraperItem


class Mixin:
    name = "zoopla"
    allowed_domains = ['zoopla.co.uk']
    start_urls = [
        ('https://www.zoopla.co.uk/to-rent/property/london/?keywords=student&price_frequency=per_month&q=London'
         '&radius=40&results_sort=newest_listings&search_source=home')]


class ZooplaParseSpider(Spider, Mixin):
    name = f"{Mixin.name}-parse"

    amenities = ['friendly', 'pets', 'smoking', 'storage', 'spacious', 'window', 'sun']
    property_types = ['Studio', 'Flat', 'House', 'Apartment', 'Maisonette', 'Room', 'bungalow', 'triplex']

    def parse(self, response):
        property_item = PropertyscraperItem()

        property_item['property_name'] = self.property_name(response)
        property_item['street_address_1'] = self.street_address(response)
        property_item['street_address_2'] = ''
        property_item['city'] = 'London'
        property_item['postcode'] = ''
        property_item['area'] = self.area(response)
        property_item['area_info'] = ''
        property_item['website'] = self.property_website(response)
        property_item['furnished'] = self.furnished(response)
        property_item['bills_included'] = self.bills_included(response)
        property_item['property_type'] = self.property_type(response)
        property_item['move_in_date'] = self.move_in_date(response)
        property_item['move_out_date'] = self.move_out_date(response)
        property_item['deposit_amount'] = self.deposit_amount(response)
        property_item['property_amenities'] = ';'.join(self.property_amenities(response))
        property_item['property_images'] = self.property_images(response)
        property_item['property_description'] = self.description(response)
        property_item['room_images'] = self.room_images(response)
        property_item['room_name'] = self.room_name(response)
        # property_item['room_availability'] = ''
        property_item['property_contact_name'] = ''
        property_item['property_contact_email'] = ''
        property_item['property_contact_number'] = self.property_contact_number(response)
        property_item['discounts'] = self.discount(response)
        property_item['room_price'] = self.room_price(response)
        property_item['floor_plans'] = self.floorplan(response)
        property_item['deposit_name'] = self.deposit_name(response)
        property_item['deposit_type'] = ''
        property_item['room_amenities'] = ';'.join(self.room_amenities(response))
        property_item['property_ad_link'] = response.url
        property_item['agent_fees'] = self.agent_fees(response)
        property_item['agent_fees_amount'] = self.agent_fees_amount(response)
        property_item['agent_name'] = self.agent_name(response)

        yield property_item

    def discount(self, response):
        description = self.combine_features_and_description(response)

        discount_info = [d for d in description if '% off' in d]
        return discount_info[0] if discount_info else ''

    def agent_name(self, response):
        return response.css('.ui-agent__name ::text').extract_first()

    def combine_features_and_description(self, response):
        property_info = self.property_amenities(response)
        property_info.extend(self.description(response))

        description = []
        for info in property_info:
            description.extend(info.split('.'))

        return description

    def agent_fees(self, response):
        return 'Yes' if self.agent_fees_amount(response) else 'No'

    def agent_fees_amount(self, response):
        fees = response.css('.ui-modal-message #dp-modal-fees-content ::text').extract()
        fee_regex = '(?:£)([\d,]+)(?:.*Fee|.*fee)'
        fee_amount = sum([int(''.join(re.findall(fee_regex, f))) for f in fees if ''.join(re.findall(fee_regex, f))])
        return f"£{fee_amount}" if fee_amount else ''

    def move_in_date(self, response):
        description = self.combine_features_and_description(response)

        move_in_info = [d for d in description if 'available' in d.lower()]

        if move_in_info:
            date = re.findall('(?:on|from|:)\s*([a-zA-Z0-9,\s]{1,17}20[\d]{2})', move_in_info[0])
            try:
                date = parser.parse(date[0])
                return date.strftime("%d/%m/%Y")
            except IndexError:
                date_info = re.findall('(?:Available|available)\s*([a-zA-Z0-9]+)', move_in_info[0])
                # pdb.set_trace()
                if re.findall('immediately|now', ''.join(date_info[0]).lower()):
                    return datetime.datetime.now().strftime("%d/%m/%Y")
                if re.findall('mid|end|beginning', ''.join(date_info[0]).lower()):
                    month = re.findall('(?:mid|end|beginning)\s*([a-zA-Z0-9]+)', move_in_info[0])
                    month = parser.parse(month[0])
                    return month.strftime("%d/%m/%Y")
        return ''

    def move_out_date(self, response):
        description = self.combine_features_and_description(response)
        move_out_info = [d for d in description if 'move out' in d]
        if len(move_out_info) > 0:
            date = re.findall('(?:to|till|:)\s*([a-zA-Z0-9,\s]{1,17}20[\d]{2})', move_out_info[0])
            try:
                date = parser.parse(date[0])
                return date.strftime("%d/%m/%Y")
            except IndexError:
                if re.findall('mid|end|beginning', ''.join(move_out_info[0]).lower()):
                    month = re.findall('(?:mid|end|beginning)\s*([a-zA-Z0-9]+)', move_out_info[0])
                    month = parser.parse(month[0])
                    return month.strftime("%d/%m/%Y")

        return ''

    def raw_deposit_info(self, response):
        # pdb.set_trace()
        description = self.combine_features_and_description(response)
        deposit = [d for d in description if 'deposit' in d.lower()]

        return deposit if deposit else ''

    def deposit_amount(self, response):
        raw_deposit = self.raw_deposit_info(response)
        if raw_deposit:
            regex = '(?:Deposit.*?|deposit.*?)(?:(£[\d,]+|\s[\d,]+\spounds)|(?:rent))'
            deposit_amount = [' '.join(list(re.findall(regex, d))) for d in raw_deposit if re.findall(regex, d)]
            if deposit_amount:
                return deposit_amount[0]
            regex = '(£\d+).*deposit'
            deposit_amount = [' '.join(list(re.findall(regex, d))) for d in raw_deposit if re.findall(regex, d)]
            if deposit_amount:
                return deposit_amount[0]
            regex = 'pay.*?(£\d+)'
            deposit_amount = [' '.join(list(re.findall(regex, d))) for d in raw_deposit if re.findall(regex, d)]
            if deposit_amount:
                return deposit_amount[0]

        return ''

    def deposit_name(self, response):
        raw_deposit = self.raw_deposit_info(response)
        deposit_name = ""
        if raw_deposit:
            regex = 'Deposit|Bond|Security|Holding'
            deposit_name = [' '.join(re.findall(regex, d)) for d in raw_deposit if re.findall(regex, d) and '£' in d]

        return deposit_name[0] if deposit_name else ''

    def room_amenities(self, response):
        descriptions = self.combine_features_and_description(response)
        amenities = [d for d in descriptions if any(a for a in self.amenities if a in d)]

        return amenities

    def floorplan(self, response):
        floorplan_css = '.dp-assets-card__item img::attr(data-src)'
        floor_plan = response.css(floorplan_css).extract_first()
        return floor_plan or 'Floorplan is not available'

    def room_price(self, response):
        price_css = '.dp-sidebar-wrapper__summary .ui-pricing__main-price ::text'
        price = response.css(price_css).extract_first()
        return ''.join(re.findall('£|\d+', price))

    def property_contact_name(self, response):
        contact_name_css = '//div[@class="sidebar sbt"]/p/strong/a/text()'
        return response.xpath(contact_name_css).extract_first()

    def property_contact_number(self, response):
        contact_number = response.xpath('//a[@data-track-label="Agent phone number 1"]/text()').extract()
        contact_number = [''.join(re.findall('\d+', self.clean_string(c))) for c in contact_number if
                          self.clean_string(c)]
        return contact_number[0] if contact_number else ''

    def property_name(self, response):
        property_amenities = self.property_amenities(response)
        property_configuration = [a for a in property_amenities if 'bedroom' in a]
        property_type = self.property_type(response) or ''

        return f"{property_configuration[0]} {property_type}" if property_configuration else f"{property_type}"

    def room_name(self, response):
        property_configuration = response.xpath('//section[@class="dp-features"]/ul[1]/li/text()').extract()
        property_configuration = [re.sub(' +', ' ', self.clean_string(pc)) for pc in property_configuration if
                                  self.clean_string(pc)]
        return ' '.join(property_configuration).title().replace('s ', ' ')

    def raw_images(self, response):
        images = response.css('.dp-gallery__list img::attr(src)').extract()
        images = [i.replace('//lid', '//lc').replace('645/430/', '') for i in images]
        return images

    def property_images(self, response):
        images = self.raw_images(response)
        property_image = response.xpath('//div[@id="images-main"]/span[not(@id)]/img/@src').extract_first()
        return images[:1] or [property_image]

    def room_images(self, response):
        images = self.raw_images(response)
        return images[1:]

    def property_type(self, response):
        property_heading = response.css('.listing-details-h1 ::text').extract_first() or response.css(
            '.ui-prop-summary__title ::text').extract_first()
        property_type = [t for t in self.property_types if t.lower() in property_heading.lower()]
        if property_type:
            return property_type[0]
        else:
            description = self.description(response)
            property_type = [t for t in self.property_types if any(d for d in description if t in d)]
            return property_type[0] if property_type else ''

    def property_amenities(self, response):
        amenities = response.css('.dp-features__list li::text').extract()
        amenities = [re.sub(' +', ' ', self.clean_string(rd)) for rd in amenities if self.clean_string(rd)]

        description_xpath = '//div[@class="bottom-plus-half"]/div[@class="top"]/descendant-or-self::text()'
        raw_description = response.xpath(description_xpath).extract()
        amenities.extend([self.clean_string(rd) for rd in raw_description if self.clean_string(rd) and '-' in rd])
        dimensions = response.css('.num-sqft ::text').extract_first()
        if dimensions:
            amenities.append(dimensions)

        return amenities

    def bills_included(self, response):
        description = self.combine_features_and_description(response)
        bills_info = [d for d in description if 'bills' in d.lower()]
        return bills_info[0] if bills_info else ''

    def street_address(self, response):
        street_address_1_css = '.dp-sidebar-wrapper__summary .ui-prop-summary__address ::text'
        # pdb.set_trace()
        return response.css(street_address_1_css).extract_first()

    def area(self, response):
        address = self.street_address(response)
        # pdb.set_trace()
        return address.split(', ')[-1]

    def property_website(self, response):
        return response.css('.ui-agent__details ::attr(href)').extract_first()

    def description(self, response):
        description_css = '.dp-description__text ::text'
        raw_description = response.css(description_css).extract()
        description = [re.sub(' +', ' ', self.clean_string(rd)) for rd in raw_description if self.clean_string(rd)]

        return list(OrderedDict.fromkeys(description))

    def clean_string(self, target_str):
        return target_str.replace('\r', '').replace('\n', '').replace('-', '').strip()

    def furnished(self, response):
        property_info = self.combine_features_and_description(response)
        furnished_info = [r for r in property_info if 'furnished' in r.lower()]
        return furnished_info[0] if furnished_info else ''


class ZooplaCrawlSpider(CrawlSpider, Mixin):
    parser = ZooplaParseSpider()

    name = f"{Mixin.name}-crawl"

    pagination_url = '//div[contains(@class, "paginate bg-muted")]/a[last()]'
    property_url = 'a.photo-hover'

    rules = [Rule(LinkExtractor(restrict_xpaths=pagination_url), callback='parse'),
             Rule(LinkExtractor(restrict_css=property_url), callback=parser.parse)]
