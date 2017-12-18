import json
import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from myfacebook.models import News


class Command(BaseCommand):

    def _clean_details(self, raw_detail):
        cleaned_detail = ''.join(detail + ' ' for detail in raw_detail)
        return cleaned_detail

    def add_arguments(self, parser):
        parser.add_argument('file_name')

    def handle(self, *args, **options):
        file_name = options['file_name']
        with open(file_name) as news_data:
            news_json = json.load(news_data)
            all_news = []
            for news in news_json:

                author, created = User.objects.get_or_create(username=news['author'])

                if created:
                    author.set_password(news['author'] + '123')
                    author.save()
                raw_date = news.get('date').split(' ')[0]
                date = datetime.datetime.strptime(raw_date, '%Y-%m-%d')
                details = self._clean_details(news['details'])
                news = News(author=author,
                            title=news.get('title', 'News'),
                            date=date.strftime('%Y-%m-%d'),
                            link=news['link'],
                            description=news['description'],
                            detail=details,
                            image_url=news['image_url'])

                all_news.append(news)
            News.objects.bulk_create(all_news)
