import json
from datetime import datetime
from json.decoder import JSONDecodeError

import mock
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from news.models import News
from twitter.models import User, ProfileDoestExist


class Command(BaseCommand):
    help = 'Get path of json file contains news objects and load into "News" Model.'

    def add_arguments(self, parser):
        parser.add_argument('publisher', help='publisher username')
        parser.add_argument('source', help='Path to news json file.')
        parser.add_argument('--truncate', action='store_true', default=False,
                            help='remove all previous News from database before adding')

    def handle(self, *args, **options):
        if options['truncate']:
            News.objects.truncate()
        news_all = self.load_json(options['source'])
        publisher = self.get_publisher(options['publisher'])
        self.create_news(news_all, publisher)

    @mock.patch('django.utils.timezone.now')
    def create_news(self, news_all, publisher, now_mock):
        for news in news_all:
            now_mock.return_value = timezone.make_aware(datetime.strptime(news['pub_date'], '%Y-%m-%d %H:%M:%S'))
            News.objects.create(
                title=news['title'],
                content=news['content'],
                image_url=news['image_url'],
                publisher=publisher,
            )

    def load_json(self, path_to_news):
        try:
            with open(path_to_news, 'r') as news_file_in:
                news = json.load(news_file_in)
        except FileNotFoundError:
            raise CommandError("Source path is not correct")
        except JSONDecodeError:
            raise CommandError("File contains corrupt data")
        return news

    def get_publisher(self, publisher_username):
        try:
            return User.objects.get_by_username(publisher_username)
        except ProfileDoestExist:
            mesg = "No User exist with username '{username}'".format(username=publisher_username)
            raise CommandError(mesg)
