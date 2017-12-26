import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, Join, TakeFirst


class Course(scrapy.Item):
    author = scrapy.Field()
    basic_price = scrapy.Field()
    categories = scrapy.Field()
    course_url = scrapy.Field()
    crawled_at = scrapy.Field()
    description = scrapy.Field()
    duration = scrapy.Field()
    external_id = scrapy.Field()
    level = scrapy.Field()
    premium_price = scrapy.Field()
    provider = scrapy.Field()
    provider_url = scrapy.Field()
    title = scrapy.Field()
    view_count = scrapy.Field()


class CourseLoader(ItemLoader):
    default_item_class = Course
    default_output_processor = TakeFirst()
    categories_out = Compose()
    description_out = Join()
