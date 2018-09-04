import scrapy


class Sport(scrapy.Item):
    name = scrapy.Field()
    schedules = scrapy.Field()


class Schedule(scrapy.Item):
    time = scrapy.Field()
    event = scrapy.Field()
    phase = scrapy.Field()


class Athlete(scrapy.Item):
    name = scrapy.Field()
    _id = scrapy.Field()
    img_url = scrapy.Field()
    country = scrapy.Field()
    sport = scrapy.Field()
    height = scrapy.Field()
    age = scrapy.Field()
    weight = scrapy.Field()
    born_date = scrapy.Field()
    born_city = scrapy.Field()


class SportMedals(scrapy.Item):
    name = scrapy.Field()
    gold = scrapy.Field()
    silver = scrapy.Field()
    bronze = scrapy.Field()
    total_medals = scrapy.Field()


class CountryMedals(scrapy.Item):
    name = scrapy.Field()
    sport_medals = scrapy.Field()
