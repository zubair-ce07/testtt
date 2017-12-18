from datetime import datetime
from articles.models import Articles


class NewsscrapperPipeline(object):

    def process_item(self, item, spider):
        item['publication_date'] = datetime.strptime(
            item['publication_date'],
            '%B %d, %Y'
        )
        # Check if article is published today and not saved in database
        if is_today(item['publication_date']) and not is_exist(item['title']):
            item.save()


def is_exist(title):
    return Articles.objects.filter(title=title).exists()


def is_today(publication_date):
    if datetime.now().date() == publication_date.date():
        return True
    return False
