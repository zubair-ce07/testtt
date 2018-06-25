import re
from dateutil import parser
import datetime
from collections import OrderedDict

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
        property_item['city'] = self.city(response)
        property_item['postcode'] = self.postcode(response)
        property_item['area'] = self.area(response)
        property_item['area_info'] = self.area_rating_info(response)
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
        property_item['property_contact_name'] = self.property_contact_name(response)
        property_item['property_contact_email'] = ''
        property_item['property_contact_number'] = self.property_contact_number(response)
        property_item['discounts'] = ''
        property_item['room_price'] = self.room_price(response)
        property_item['floor_plans'] = self.floorplan(response)
        property_item['deposit_name'] = self.deposit_name(response)
        property_item['deposit_type'] = ''
        property_item['room_amenities'] = ';'.join(self.room_amenities(response))
        property_item['property_ad_link'] = response.url
        property_item['agent_fees'] = self.agent_fees(response)
        property_item['agent_fees_amount'] = ''
        property_item['agent_name'] = self.agent_name(response)

        yield property_item

    def agent_name(self, response):
        return response.css('.sidebar strong a::text').extract_first()

    def combine_features_and_description(self, response):
        property_info = self.property_info(response)
        property_info.extend(self.description(response))
        property_info.extend(self.property_amenities(response))
        description = []
        for info in property_info:
            description.extend(info.split('.'))

        return description

    def agent_fees(self, response):
        description = self.combine_features_and_description(response)
        agent_fees_info = [d for d in description if 'agent fee' in d.lower()]
        raw_desc = ''.join(agent_fees_info)
        if not raw_desc:
            return ''
        return 'No' if 'No' in raw_desc else 'Yes'

    def move_in_date(self, response):
        description = self.combine_features_and_description(response)

        move_in_info = [d for d in description if 'available' in d.lower()]

        if move_in_info:
            date = re.findall('(?:in|on|from|:)\s*([a-zA-Z0-9,\s]{1,17}20[\d]{2})', move_in_info[0])
            try:
                date = parser.parse(date[0])
                return date.strftime("%d/%m/%Y")
            except IndexError:
                date_info = re.findall('(?:Available|available)\s*([a-zA-Z0-9]+)', move_in_info[0])
                if 'now' or 'immediately' in ''.join(date_info[0]).lower():
                    return datetime.datetime.now().strftime("%d/%m/%Y")
                if 'mid' or 'end' or 'beginning' in ''.join(date_info[0]).lower():
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
                if 'mid' or 'end' or 'beginning' in ''.join(move_out_info[0]).lower():
                    month = re.findall('(?:mid|end|beginning)\s*([a-zA-Z0-9]+)', move_out_info[0])
                    month = parser.parse(month[0])
                    return month.strftime("%d/%m/%Y")

        return ''

    def raw_deposit_info(self, response):
        description = self.combine_features_and_description(response)

        deposit = [d for d in description if 'deposit' in d.lower()]
        return deposit[0] if deposit else ''

    def deposit_amount(self, response):
        raw_deposit = self.raw_deposit_info(response)
        deposit_amount = ''
        if raw_deposit:
            deposit_amount = re.findall('Deposit.*(£[\d,]+)', raw_deposit)

        return deposit_amount[0] if deposit_amount else ''

    def deposit_name(self, response):
        raw_deposit = self.raw_deposit_info(response)
        if raw_deposit and '£' in raw_deposit:
            return ' '.join(re.findall('Deposit|Bond|Security|Holding', raw_deposit[0]))

    def room_amenities(self, response):
        descriptions = self.combine_features_and_description(response)
        amenities = [d for d in descriptions if any(a for a in self.amenities if a in d)]

        return amenities

    def floorplan(self, response):
        floorplan_xpath = '//ul[contains(@class, "listing-content")]/li[/span[contains(text(), "floorplan")]]/a/@href'
        floorplan_tab_css = '#tab-floorplan img::attr(src)'
        floor_plan = response.xpath(floorplan_xpath).extract_first() or response.css(floorplan_tab_css).extract_first()

        return floor_plan or 'Floorplan is not available'

    def room_price(self, response):
        price_css = '.listing-details-price strong::text'
        price = response.css(price_css).extract_first()
        return ''.join(re.findall('£|\d+', price))

    def property_contact_name(self, response):
        contact_name_css = '//div[@class="sidebar sbt"]/p/strong/a/text()'
        return response.xpath(contact_name_css).extract_first()

    def property_contact_number(self, response):
        return response.css('.agent_phone a::text').extract_first()

    def property_name(self, response):
        property_configuration = response.css('.num-beds::attr(title)').extract_first(default='')
        property_type = self.property_type(response) or ''

        return f"{property_configuration} {property_type}"

    def room_name(self, response):
        property_configuration = response.css('.listing-details-attr span::attr(title)').extract()
        return ' '.join(property_configuration).title().replace('s ', ' ')

    def raw_images(self, response):
        return response.css('a.images-thumb ::attr(data-photo)').extract()

    def property_images(self, response):
        images = self.raw_images(response)
        property_image = response.xpath('//div[@id="images-main"]/span[not(@id)]/img/@src').extract_first()
        return images[:1] or [property_image]

    def room_images(self, response):
        images = self.raw_images(response)
        return images[1:]

    def property_type(self, response):
        property_heading = response.css('.listing-details-h1 ::text').extract_first()
        property_type = [t for t in self.property_types if t.lower() in property_heading.lower()]
        if property_type:
            return property_type[0]
        else:
            description = self.description(response)
            property_type = [t for t in self.property_types if any(d for d in description if t in d)]
            return property_type[0] if property_type else ''

    def property_amenities(self, response):
        amenities_xpath = '//div[contains(@class,"ui-tabs-panel")]/div[@class="clearfix"]/ul/li/text()'
        amenitites = response.xpath(amenities_xpath).extract()
        description_xpath = '//div[@class="bottom-plus-half"]/div[@class="top"]/descendant-or-self::text()'
        raw_description = response.xpath(description_xpath).extract()
        amenitites.extend([self.clean_string(rd) for rd in raw_description if self.clean_string(rd) and '-' in rd])

        return response.xpath(amenities_xpath).extract()

    def bills_included(self, response):
        description = self.combine_features_and_description(response)
        bills_info = [d for d in description if 'bills' in d.lower()]
        return bills_info[0] if bills_info else ''

    def postcode(self, response):
        post_code_xpath = '//meta[@property="og:postal-code"]/@content'
        return response.xpath(post_code_xpath).extract_first()

    def street_address(self, response):
        street_address_1_css = '.listing-details-address h2 ::text'
        return response.css(street_address_1_css).extract_first()

    def city(self, response):
        locality_xpath = '//meta[@property="og:locality"]/@content'
        street_xpath = '//meta[@property="og:street-address"]/@content'
        return response.xpath(locality_xpath).extract_first() or response.xpath(street_xpath).extract_first()

    def area(self, response):
        raw_area = response.css('.split2r .bottom-half ::text').extract_first().split(' ')[-1]
        return ''.join(re.findall('[a-zA-Z0-9]+', raw_area))

    def area_rating_info(self, response):
        rating_bar_style = response.css('.top-half ::attr(style)').extract_first()
        rating_bar_width = ''.join(re.findall('[0-9]+', rating_bar_style))
        return f"{int(rating_bar_width) / 20} stars"

    def property_website(self, response):
        raw_url = response.css('.sidebar strong a::attr(href)').extract_first()
        return f"https://zoopla.co.uk{raw_url}"

    def description(self, response):
        description_xpath = '//div[@class="bottom-plus-half"]/div[@class="top"]/descendant-or-self::text()'
        raw_description = response.xpath(description_xpath).extract()
        description = [self.clean_string(rd) for rd in raw_description if self.clean_string(rd)]
        return list(OrderedDict.fromkeys(description))

    def clean_string(self, target_str):
        return target_str.replace('\r', '').replace('\n', '').replace('-', '').strip()

    def furnished(self, response):
        property_info = self.combine_features_and_description(response)
        furnished_info = [r for r in property_info if 'furnished' in r.lower()]
        return furnished_info[0] if furnished_info else ''

    def property_info(self, response):
        property_info_xpath = '//ul[@class="listing-content clearfix noprint"]/li/descendant-or-self::text()'
        info = response.xpath(property_info_xpath).extract()
        return [self.clean_string(r) for r in info if self.clean_string(r)]


class ZooplaCrawlSpider(CrawlSpider, Mixin):
    parser = ZooplaParseSpider()

    name = f"{Mixin.name}-crawl"

    pagination_url = '//div[contains(@class, "paginate bg-muted")]/a[last()]'
    property_url = 'a.photo-hover'

    rules = [Rule(LinkExtractor(restrict_xpaths=pagination_url), callback='parse'),
             Rule(LinkExtractor(restrict_css=property_url), callback=parser.parse)]
