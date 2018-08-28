from re import findall

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from Asiangames_Scrapy.items import Sport, Schedule


class AsianGamesSpider(CrawlSpider):

    name = 'AsianGamesSpider'
    domain = ['https://en.asiangames2018.id/']
    start_urls = [
        'https://en.asiangames2018.id/sport/',
    ]
    rules = (
        Rule(LinkExtractor(restrict_css='.or-sportshub__item'), callback='parse_sport_item'),
        Rule(LinkExtractor(restrict_css='.or-athletes__list'), callback='parse_athletes')
    )

    def parse_sport_item(self, response):
        all_links = self._sport_urls(response)
        athletes_link, schedule_link = all_links

        sport_item = Sport()
        sport_item['name'] = self._sport_name(response)
        sport_item['athletes'] = []
        sport_item['schedules'] = []
        sport_item['schedule_link'] = self._complete_url(schedule_link)

        meta = {}
        meta['sport_item'] = sport_item

        url = self._complete_url(athletes_link)
        return Request(
            url=url, callback=self.parse_athletes, meta=meta
        )

    def parse_athletes(self, response):
        sport_item = response.meta['sport_item']

        for athlete_item in self._athlete_items(response):

            athlete = {}
            athlete['name'] = self._athlete_name(athlete_item)
            athlete['id'] = self._athlete_id(athlete_item)
            athlete['img_url'] = self._athlete_image(athlete_item)
            athlete['country'] = self._athlete_country(athlete_item)
            sport_item['athletes'].append(athlete)

        next_page_link = self._athlete_next_page_link(response)

        meta = {}
        meta['sport_item'] = sport_item

        if next_page_link:

            url = self._complete_url(next_page_link)
            return Request(
                url=url, callback=self.parse_athletes, meta=meta
            )
        else:

            schedule_link = sport_item['schedule_link']
            del sport_item['schedule_link']
            return Request(
                url=schedule_link, callback=self.parse_schedule, meta=meta
            )

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

    def _schedule_items(self, response):
        return response.css('.or-disc-day-wrap')

    def _schedule_main_day(self, response):
        return response.css('.or-disc-title::text').extract_first()

    def _schedule_day_list(self, response):
        return response.css('.or-ses-list')

    def _schedule_time(self, response):
        return response.css('td time span:last-child::text').extract_first().strip()

    def _schedule_event(self, response):
        return response.css('td span.or-evt-phase_evt::text').extract_first()

    def _schedule_phase(self, response):
        return response.css('td span.or-evt-phase_ph::text').extract_first()

    def _sport_name(self, response):
        return response.css('span.or-h-disc-name::text').extract_first().strip()

    def _sport_urls(self, response):
        return response.css('.or-sidecol .or-sp-details-list:last-child a::attr(href)').extract()

    def _athlete_items(self, response):
        return response.css('.or-athletes__item')

    def _athlete_name(self, response):
        return response.css('.or-card-athlete__name::attr(title)').extract_first()

    def _athlete_id(self, response):
        output = response.css('.or-athletes__link::attr(href)').extract_first()
        return findall(r'\d+', output)[0]

    def _athlete_image(self, response):
        return response.css('.or-card-athlete__photo img::attr(src)').extract_first()

    def _athlete_country(self, response):
            return response.css('.or-card-athlete__country img::attr(alt)').extract_first()

    def _athlete_next_page_link(self, response):
        return response.css('.or-cta__btn--next::attr(href)').extract_first()

    def _complete_url(self, url):
        return self.domain[0][:-1] + url
