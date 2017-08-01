import json
from django.core.management.base import BaseCommand
from cinescore.models import Category, Movie, Website, Rating


class Command(BaseCommand):
    help = 'Create a new user'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('backup/ratings.json') as rating_file:
            rating_data = json.load(rating_file)
        for rating_obj in rating_data:
            movie = rating_obj['movie']
            poster = movie['poster']
            content_rating = movie['content_rating']
            title = movie['title']
            date_of_release = movie['date_of_release']
            plot = movie['plot']
            movie_id = movie['movie_id']
            categories = movie['category']
            movie_obj, created = Movie.objects.get_or_create(movie_id=movie_id, title=title,
                                                             content_rating=content_rating,
                                                             date_of_release=date_of_release, plot=plot, poster=poster)
            cat_objs = []
            for category_dict in categories:
                obj, created = Category.objects.get_or_create(category_name=category_dict['category_name'])
                cat_objs.append(obj)
            if cat_objs:
                c = movie_obj.category.add(*cat_objs)
            provider_website = rating_obj['provider_website']
            web, created = Website.objects.get_or_create(url=provider_website['url'], name=provider_website['name'])
            rating = rating_obj['rating'] or 0
            rating = float(rating.strip(' "'))
            target_url = rating_obj['target_url']
            rating_obj_created, created = Rating.objects.update_or_create(movie=movie_obj, provider_website=web,
                                                                          rating=rating, target_url=target_url)
