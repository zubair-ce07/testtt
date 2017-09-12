from django.db import models
from django.utils import timezone
from movies.models import Movie, Role
from users.models import User


class WatchListItem(models.Model):
    LIKED = 1
    DISLIKED = 2

    RATINGS = (
        (LIKED, 'Like'),
        (DISLIKED, 'Disliked')
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlist_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    removed = models.BooleanField(default=False)
    is_watched = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(choices=RATINGS, null=True, blank=True)
    best_actor = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, related_name='votes')
    is_recommended = models.BooleanField(default=False)


class Activity(models.Model):
    ADDED = 1
    WATCHED = 2
    RATED = 3
    VOTED_ACTOR = 4
    RECOMMENDED = 5

    TYPES = (
        (ADDED, 'Added'),
        (WATCHED, 'Watched'),
        (RATED, 'Rated'),
        (VOTED_ACTOR, 'Voted Actor'),
        (RECOMMENDED, 'Recommended')
    )

    watchlist = models.ForeignKey(WatchListItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    type = models.PositiveSmallIntegerField(choices=TYPES)

    class Meta:
        ordering = ['-created_at']
