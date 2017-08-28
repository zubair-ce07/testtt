import scrapy


class ProfileItem(scrapy.Item):
    employmentHistory = scrapy.Field()
    overview = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    skills = scrapy.Field()
    tests = scrapy.Field()
    assignments = scrapy.Field()
    portfolios = scrapy.Field()
    education = scrapy.Field()
    url = scrapy.Field()
    workHistory = scrapy.Field()
    title = scrapy.Field()
    identity = scrapy.Field()


class CompanyItem(scrapy.Item):
    overview = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    assignments = scrapy.Field()
    url = scrapy.Field()
    workHistory = scrapy.Field()
    title = scrapy.Field()
    managers = scrapy.Field()
    website = scrapy.Field()
