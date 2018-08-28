import scrapy


class Sport(scrapy.Item):
    name = scrapy.Field()
    athletes = scrapy.Field()
    schedules = scrapy.Field()
    schedule_link = scrapy.Field()

class Schedule(scrapy.Item):
    time = scrapy.Field()
    event = scrapy.Field()
    phase = scrapy.Field()
