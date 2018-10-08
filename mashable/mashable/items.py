import scrapy


class Story(scrapy.Item):
    story_id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    published_date = scrapy.Field()
    video_link = scrapy.Field()
    link = scrapy.Field()
    cover_image = scrapy.Field()
