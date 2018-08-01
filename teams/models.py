from django.db import models
from teams.choices import BattingStyleChoices, BowlingStyleChoices, PlayingRoleChoices, FormatChoices, TeamTypeChoices
from datetime import date
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from common.models import SoftDeleteModelMixin


class Team(SoftDeleteModelMixin):
    name = models.CharField(max_length=50, default=' ')
    ranking = models.IntegerField(default=0)
    type = models.CharField(max_length=20, choices=TeamTypeChoices.Choices)
    url = models.URLField(max_length=100, default=' ')
    photos = GenericRelation('Photo', related_query_name='teams')

    def __str__(self):
        return self.name


class Player(SoftDeleteModelMixin):

    name = models.CharField(max_length=100, default=' ')
    DOB = models.DateField('Born')
    playing_role = models.CharField(max_length=20, default=' ', choices=PlayingRoleChoices.Choices)
    batting_style = models.CharField(max_length=20, default=' ', choices=BattingStyleChoices.Choices)
    bowling_style = models.CharField(max_length=30, default=' ', choices=BowlingStyleChoices.Choices)
    ranking = models.PositiveSmallIntegerField(null=True, blank=True)
    teams = models.ManyToManyField('Team', related_name='players', blank=True)
    url = models.URLField(max_length=100, default=' ', null=True, blank=True)
    photos = GenericRelation('Photo', related_query_name='players')

    def __str__(self):
        return self.name

    @property
    def get_age(self):
        today = date.today()
        cal_age = today.year - self.DOB.year - ((today.month, today.day) < (self.DOB.month, self.DOB.day))
        return cal_age


class BasicAverageInfo(SoftDeleteModelMixin):

    format = models.CharField(max_length=50, choices=FormatChoices.Choices)
    matches = models.IntegerField(null=True, blank=True)
    innings = models.IntegerField(null=True, blank=True)

    runs = models.IntegerField(null=True, blank=True)
    average = models.FloatField(null=True, blank=True)
    strike_rate = models.FloatField(null=True, blank=True)
    balls = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class BattingAverage(BasicAverageInfo):

    player = models.ForeignKey(Player, related_name='batting_averages', on_delete=models.CASCADE)

    not_outs = models.IntegerField(null=True, blank=True)
    highest_score = models.CharField(max_length=50, default=' ')    # 88*
    hundreds = models.IntegerField(null=True, blank=True)
    fifties = models.IntegerField(null=True, blank=True)
    fours = models.IntegerField(null=True, blank=True)
    sixes = models.IntegerField(null=True, blank=True)
    catches = models.IntegerField(null=True, blank=True)
    stumps = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{player_name}\'s batting average'.format(
            player_name=self.player
        )


class BowlingAverage(BasicAverageInfo):
    player = models.ForeignKey(Player, related_name='bowling_averages', on_delete=models.CASCADE)

    wickets = models.IntegerField(null=True, blank=True)
    best_bowling_innings = models.CharField(max_length=50, default=' ', null=True, blank=True)
    best_bowling_match = models.CharField(max_length=50, default=' ', null=True, blank=True)
    economy = models.FloatField(null=True, blank=True)
    four_wickets = models.IntegerField(null=True, blank=True)
    five_wickets = models.IntegerField(null=True, blank=True)
    ten_wickets = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{player_name}\'s bowling average'.format(
            player_name=self.player
        )


class Photo(models.Model):
    limit = models.Q(app_label='articles', model='article') | models.Q(app_label='teams', model='player') | \
            models.Q(app_label='teams', model='team') | models.Q(app_label='users', model='profile')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    photo_url = models.URLField(max_length=100, default=' ')
    photo = models.ImageField(upload_to="", blank=False)


class LiveScore(models.Model):
    team1 = models.ForeignKey(Team, related_name='lives_scores_1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='lives_scores_2', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True, blank=True)
