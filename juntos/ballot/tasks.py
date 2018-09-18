from __future__ import absolute_import, unicode_literals

from celery.decorators import task

from .models import Ballot


@task(name="update_ballots_status", bind=True)
def update_ballots_status(self):
    """
    Checks if any ballot's status need to be updated in case ending ballot date-time comes.
    """
    active_ballots = Ballot.objects.get_active_ballots()

    for ballot in active_ballots:
        if not ballot.should_remain_active:
            ballot.is_active = False
            ballot.save()
