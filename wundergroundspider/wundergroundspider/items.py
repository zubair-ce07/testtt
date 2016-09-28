import scrapy


class WeatherItem(scrapy.Item):
    year = scrapy.Field()
    month = scrapy.Field()
    city = scrapy.Field()
    weather_rows = scrapy.Field()
    pass
