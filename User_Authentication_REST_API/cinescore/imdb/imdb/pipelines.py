# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from cinescore.models import Movie, Category, Rating, Website


class ImdbPipeline(object):
    def process_item(self, item, spider):
        categories = []
        for category in item['categories']:
            obj, created = Category.objects.get_or_create(category_name=category)
            import pdb; pdb.set_trace()
            categories.append(obj)
        import pdb;
        pdb.set_trace()
        content_rating = item['content_rating']
        poster = item['poster']
        release_date = item['release_date'] or "Unknown"
        title = item['title']
        movie_id = item['movie_id']
        movie = Movie.objects.create(movie_id=movie_id, title=title, content_rating=content_rating,
                                     date_of_release=release_date, poster=poster)
        movie.category.add(*categories)

        website_base_url = item['base_url']
        rating = item['rating']
        rating = float(rating.strip(' "'))
        url = item['url']
        web, created = Website.objects.get_or_create(url=website_base_url, name=website_base_url.split(".")[1])
        rating = Rating.objects.update_or_create(movie=movie, website_base_url=web,
                                                 rating=rating, website_url=url)
        return item

