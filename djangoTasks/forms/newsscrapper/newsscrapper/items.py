from scrapy_djangoitem import DjangoItem
from articles.models import Articles


class NewsArticleItem(DjangoItem):

    django_model = Articles
