from re import findall

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from Asiangames_Scrapy.items import *


class AsianGamesSpider(CrawlSpider):
    """
    AsianGamesSpider extracts all the athletes, sports and medal records from
    the asian games official site
    """

    name = 'AsianGamesSpider'
    domains = ['https://en.asiangames2018.id/']
    start_urls = [
        'https://en.asiangames2018.id/athletes/',
        'https://en.asiangames2018.id/sport/',
        'https://en.asiangames2018.id/medals/',
    ]

    athlete_css_rule = '.or-athletes__list'
    sport_item_css_rule = '.or-sportshub__list'
    medals_css_rule = '.or-ses-list'
    athlete_next_page_css_rule = '.or-cta__btn--next'

    sport_item_regex = r'^(https://en.asiangames2018.id/)sport/[a-zA-z]+/'
    medals_regex = r'^(https://en.asiangames2018.id/)medals/[a-zA-z]+/'

    rules = (
        Rule(LinkExtractor(
            restrict_css=athlete_css_rule), callback='parse_athlete'
        ),
        Rule(LinkExtractor(
            restrict_css=sport_item_css_rule, allow=sport_item_regex),
            callback='parse_sport_item'
        ),
        Rule(LinkExtractor(
            restrict_css=medals_css_rule, allow=medals_regex),
            callback='parse_medals'
        ),
        Rule(LinkExtractor(restrict_css=athlete_next_page_css_rule))
    )

    def parse_sport_item(self, response):
        schedule_link = self._complete_url(self._sport_urls(response))

        sport_item = Sport()
        sport_item['name'] = self._sport_name(response)
        sport_item['schedules'] = []

        meta = {}
        meta['sport_item'] = sport_item

        return Request(
            url=schedule_link, callback=self.parse_schedule, meta=meta
        )

    def parse_athlete(self, response):
        athlete = Athlete()
        athlete['name'] = self._athlete_name(response)
        athlete['_id'] = self._athlete_id(response)
        athlete['img_url'] = self._athlete_image(response)
        athlete['country'] = self._athlete_country(response)
        athlete['sport'] = self._athlete_sport(response)
        athlete['height'] = self._athlete_height(response)
        athlete['age'] = self._athlete_age(response)
        athlete['weight'] = self._athlete_weight(response)
        athlete['born_date'] = self._athlete_born_date(response)
        athlete['born_city'] = self._athlete_born_city(response)
        return athlete

    def parse_schedule(self, response):
        sport_item = response.meta['sport_item']

        for schedule_item in self._schedule_items(response):
            main_day = self._schedule_main_day(schedule_item)
            day_schedules = []

            for day_list_item in self._schedule_day_list(schedule_item):
                schedule = Schedule()
                schedule['time'] = self._schedule_time(day_list_item)
                schedule['event'] = self._schedule_event(day_list_item)
                schedule['phase'] = self._schedule_phase(day_list_item)
                day_schedules.append(schedule)

            sport_item['schedules'].append({main_day: day_schedules})

        return sport_item

    def parse_medals(self, response):
        country_medals = CountryMedals()
        country_medals['name'] = self._medals_country_name(response)
        country_medals['sport_medals'] = []

        for medal_sport_row in self._medal_sport_rows(response):
            sport_medals = SportMedals()
            sport_medals['name'] = self._medals_sport_name(medal_sport_row)
            gold, silver, bronze, total = self._medals_sports_count(medal_sport_row)
            sport_medals['gold'] = gold
            sport_medals['silver'] = silver
            sport_medals['bronze'] = bronze
            country_medals['sport_medals'].append(sport_medals)

        return country_medals

    def _schedule_items(self, response):
        return response.css('.or-disc-day-wrap')

    def _schedule_main_day(self, response):
        return response.css('.or-disc-title::text').extract_first()

    def _schedule_day_list(self, response):
        return response.css('.or-ses-list')

    def _schedule_time(self, response):
        output = response.css('span[data-or-onlytime]::text').extract_first()
        if output:
            return output.strip()

    def _schedule_event(self, response):
        return response.css('td span.or-evt-phase_evt::text').extract_first()

    def _schedule_phase(self, response):
        return response.css('td span.or-evt-phase_ph::text').extract_first()

    def _sport_name(self, response):
        return response.css('span.or-h-disc-name::text').extract_first().strip()

    def _sport_urls(self, response):
        css_rule = '.or-sidecol .or-sp-details-list:last-child a::attr(href)'
        return response.css(css_rule).extract()[1]

    def _athlete_items(self, response):
        return response.css('.or-athletes__item')

    def _athlete_name(self, response):
        name = response.css('.or-athlete-profile__name--name::text').extract_first()
        surname = response.css('.or-athlete-profile__name--surname::text').extract_first(default='')
        return '{} {}'.format(name, surname)

    def _athlete_id(self, response):
        return findall(r'\d+', response.url)[1]

    def _athlete_image(self, response):
        return response.css('.or-athlete-profile__pic img::attr(src)').extract_first()

    def _athlete_profile_url(self, response):
        return response.css('.or-athletes__link::attr(href)').extract_first()

    def _athlete_country(self, response):
        return response.css('.or-athlete-profile__nationality--flag::attr(alt)').extract_first()

    def _athlete_next_page_link(self, response):
        return response.css('.or-cta__btn--next::attr(href)').extract_first()

    def _complete_url(self, url):
        # to remove the last slash(/)
        return self.domains[0][:-1] + url

    def _athlete_sport(self, response):
        return response.css('.or-athlete-profile__discipline::text').extract_first()

    def _athlete_height(self, response):
        css_rule = '.or-anagraphic__block .or-anagraphic__data'
        output = response.css(css_rule)[2].css('::text').extract_first().strip()
        matched_output = findall(r'\d+', output)
        if matched_output:
            return matched_output[0]

    def _athlete_age(self, response):
        return response.css('.or-anagraphic__block .or-anagraphic__data::text').extract()[0].strip()

    def _athlete_weight(self, response):
        css_rule = '.or-anagraphic__block .or-anagraphic__data'
        output = response.css(css_rule)[3].css('::text').extract_first().strip()
        matched_output = findall(r'\d+', output)
        if matched_output:
            return matched_output[0]

    def _athlete_born_date(self, response):
        return response.css('.or-athlete__birth--date::text').extract_first()

    def _athlete_born_city(self, response):
        return response.css('.or-athlete__birth--city::text').extract_first()

    def _medals_country_name(self, response):
        return response.css('.or-country-header h2::text').extract_first()

    def _medal_sport_rows(self, response):
        return response.css('#or-tbl-country-medal .or-table-list-groupedRow')

    def _medals_sport_name(self, response):
        return response.css('a::attr(title)').extract_first()

    def _medals_sports_count(self, response):
        return response.css('.or-md::text').extract()
