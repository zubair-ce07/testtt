from __future__ import absolute_import, unicode_literals
from datetime import datetime, timedelta

from celery import task
from django.conf import settings

from dashboard.models import Offers


@task()
def expire_offers_week_ago():
    """Run daily at midnight
    Mark all the offers that are active and older
    than a week as 'expired'
    """
    if settings.DEBUG:
        print("TASK: checking offer for expiry")

    date_week_ago = datetime.now() - timedelta(days=7)
    expired_offers = Offers.objects.filter(
        created_at__lte=date_week_ago,
        status='active'
        )
    if not expired_offers.exists():
        return False

    # marked status as expired
    expired_offers.update(status="expired")

    return True